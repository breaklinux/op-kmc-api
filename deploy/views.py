from deploy import base, docker, master, node, server_resource
from django.http import JsonResponse
from tools.datetime_tools import runTime,runTimeCalculate
from tools.ssh_channel import sshChannelManager
import paramiko
import json

# 配置ssh登录linux客户端
def sshLinux(host, port, username, password, hostname, ip, logsize, registries, deploy):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if deploy != 1:  # 这里接收master的ip、用户名及密码
        ssh_client.connect(hostname=ip, port=port, username=username, password=password)
        cmd = master.joinTokenNew()  # 获取token命令(最新)
        out = sshCmd(ssh_client, cmd)
        master.saveTokenFile(out)  # 存入本地
        if deploy == 2:  # 执行拷贝master节点pki命令
            pass
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    if deploy == 1 or deploy == 2 or deploy == 3:
        # 基础配置(1、2、3都走)
        print("系统基本配置及参数优化中......")
        startDeployTime = runTime()
        base.saveFile(hostname, ip)
        cmd = base.deployBase(hostname, ip)
        for c in cmd:
            sshCmd(ssh_client, c)
        endDeployTime = runTime()
        runTimeCalculate("系统基础配置+参数优化耗时: ", endDeployTime, startDeployTime)

        # docker安装(1、2、3都走)
        print("docker环境部署中......")
        startDockerDeployTime = runTime()
        cmd = docker.deployDocker(logsize, registries)
        for c in cmd:
            sshCmd(ssh_client, c)
        endDockerDeployTime = runTime()
        runTimeCalculate("Docker环境部署耗时: ", endDockerDeployTime, startDockerDeployTime)

        # 安装master(deploy：1为需要init，deploy：2为加入master节点)
        startK8sMasterDeployTime = runTime()
        # docker安装(1、2、3都走)
        print("docker环境部署中......")
        cmd = docker.deployDocker(logsize, registries)
        for c in cmd:
            sshCmd(ssh_client, c)

        # 安装master(deploy：1为需要init，deploy：2为加入master节点)
        if deploy == 1 or deploy == 2:
            print("master环境部署中......")
            cmd = master.yumKube()  # 部署
            sshCmd(ssh_client, cmd)
            if deploy == 1:
                cmd = master.kubeInit(ip)  # 初始化
                sshCmd(ssh_client, cmd)
                cmd = master.joinToken()  # 获取jointoken命令
                out = sshCmd(ssh_client, cmd)
                master.saveTokenFile(out)  # 存入本地
                cmd = master.kubectlPermission()  # 配置kubectl
                sshCmd(ssh_client, cmd)
                cmd = master.flannel()  # 部署flannel
                sshCmd(ssh_client, cmd)
            elif deploy == 2:
                cmd = master.joinMasterCluster()  # 获取jointoken命令后执行加入
                sshCmd(ssh_client, cmd)
                cmd = master.kubectlPermission()  # 配置kubectl
                sshCmd(ssh_client, cmd)
        endK8SMasterDeployTime = runTime()
        runTimeCalculate("k8s-master部署耗时: ", endK8SMasterDeployTime, startK8sMasterDeployTime)

        # 安装node(deploy：3为node节点)
        startNodeTime = runTime()
        if deploy == 3:
            print("node环境部署中......")
            cmd_list = []
            cmd_list.append(node.yumKube())
            cmd_list.append(node.joinMasterCluster())
            for c in cmd_list:
                sshCmd(ssh_client, c)
        endNodeTime = runTime()
        runTimeCalculate("k8s-node部署耗时: ", endNodeTime, startNodeTime)

    # 服务器基本信息返回
    print("返回服务基本信息")
    data = {}
    df = server_resource.df(ssh_client)
    cpu = server_resource.cpu(ssh_client)
    mem = server_resource.mem(ssh_client)
    data["code"] = 0
    data["messgae"] = "k8s v1.23.5 version deploy success"
    data["Disk"] = df
    data["Cpu"] = cpu
    data["Mem"] = mem
    print(data)
    ssh_client.close()
    return data


def sshDeploy(request):
    methodResponseMsg = """{method} Method not supported""".format(method=request.method)
    if request.method == "GET":
        return JsonResponse(standardResponse(methodResponseMsg))
    elif request.method == "POST":
        data = json.loads(request.body)
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        hostname = data.get('hostname')
        ip = data.get('ip')  # master 以及 apiserver的ip
        logsize = data.get('logsize')
        registries = data.get('registries')
        deploy = data.get('deploy')
        data = sshLinux(host, port, username, password, hostname, ip, logsize, registries, deploy)
        return JsonResponse(data)
    else:
        return JsonResponse(standardResponse(methodResponseMsg))


"""
 1.公共返回数据格式
"""


def standardResponse(msg=None, token=None):
    if not token:
        data = {"code": 1, "message": msg, "data": {"token": "", "state": "false"}}
    else:
        data = {"code": 0, "message": msg, "data": {"token": token, "state": "true"}}
    return data
