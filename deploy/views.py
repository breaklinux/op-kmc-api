from deploy import base,docker,master,node,server_resource
import paramiko,json


def sshCmd(ssh_client,c):
    print("执行命令:{0}".format(c))
    stdin, stdout, stderr = ssh_client.exec_command(c,get_pty=True)
    if not stdout is None:
        return stdout.read()
    if not stderr is None:
        return stderr.read()

#配置ssh登录linux客户端
def sshLinux(host,port,username,password,hostname,ip,logsize,registries,deploy):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    if deploy == 1 or deploy == 2 or deploy == 3:
        #基础配置(1、2、3都走)
        print("系统基本配置及参数优化中......")
        base.saveFile(hostname, ip)
        cmd=base.deployBase(hostname,ip)
        for c in cmd:
            o = sshCmd(ssh_client,c)
            print("命令执行结果：" + str(o))

        #docker安装(1、2、3都走)
        print("docker环境部署中......")
        cmd=docker.deployDocker(logsize,registries)
        for c in cmd:
            o = sshCmd(ssh_client,c)
            print("命令执行结果：" + str(o))

        # 安装master(deploy：1为需要init，deploy：2为加入master节点)
        if deploy == 1 or deploy ==2:
            print("master环境部署中......")
            cmd=master.yumKube()  #部署
            o = sshCmd(ssh_client, cmd)
            print("命令执行结果：" + str(o))
            if deploy == 1:
                cmd = master.kubeInit(ip)  #初始化
                o = sshCmd(ssh_client,cmd)
                print("命令执行结果：" + str(o))
                cmd = master.joinToken()   #获取jointoken命令
                out = sshCmd(ssh_client,cmd)
                master.saveTokenFile(out)# 存入本地
            elif deploy == 2:
                cmd = master.joinTokenNew()  #获取token命令(最新)
                out = sshCmd(ssh_client,cmd)
                master.saveTokenFile(out)# 存入本地
                cmd = master.joinMasterCluster()# 获取jointoken命令后执行加入
                sshCmd(ssh_client,cmd)
            master.kubectlPermission()   #配置kubectl
            master.flannel()  #配置flannel
            o = sshCmd(ssh_client, c)
            print("命令执行结果：" + str(o))

        # 安装node(deploy：3为node节点)
        if deploy == 3:
            print("node环境部署中......")
            cmd_list=[]
            cmd_list.append(node.yumKube())
            cmd_list.append(node.joinMasterCluster())
            for c in cmd_list:
                o = sshCmd(ssh_client,c)
                print("命令执行结果：" + str(o))

    #服务器基本信息返回
    print("返回服务基本信息")
    data={}
    df = server_resource.df(ssh_client)
    cpu = server_resource.cpu(ssh_client)
    mem = server_resource.mem(ssh_client)
    data["Disk"] = df
    data["Cpu"] = cpu
    data["Mem"] = mem

    ssh_client.close()

def sshDeploy(request):
    if request.method == "POST":
        data = json.loads(request.body)
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        hostname = data.get('hostname')
        ip = data.get('ip')
        logsize = data.get('logsize')
        registries = data.get('registries')
        deploy = data.get('deploy')
        sshLinux(host, port, username, password, hostname, ip, logsize, registries, deploy)