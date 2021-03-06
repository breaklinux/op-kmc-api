# master安装
import os
import csv

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_k8s_master_celery")  # 获取当前path路径
base = os.path.join(HOME_DIR, "base")
os.sys.path.append(script_path)
os.sys.path.append(base)
from .main import app
from ssh_channel import sshChannelManager
from deploy.views import k8sDeployCluster


# 安装kubeadm、kubelet、kubectl，并设置开机自启
def yumKube():
    cmd = "sudo rpm -qa |grep -E 'kubelet|kubeadm|kubectl|kubernetes-cni'|xargs rpm -e; sudo yum install -y kubelet-1.23.5-0 kubeadm-1.23.5-0 kubectl-1.23.5-0;sudo systemctl enable kubelet.service"
    return cmd

# 清理现有规则
def cleanK8SRole():
    cmd = "sudo yes|kubeadm reset; sudo rm -rf /etc/cni/net.d; sudo iptables -F; sudo iptables -X ;sudo rm -f $HOME/.kube/config; sudo rm -f ~/kube-init.log"
    return cmd

# kubeadm init 初始化(只有第一次部署master需要，需要参数deploy:1)，ip为kubeapi的地址
def kubeInit(ip):
    cmd = "sudo kubeadm init --v=5 --apiserver-advertise-address=" + str(
        ip) + " --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.23.5 --service-cidr=10.1.0.0/16 --pod-network-cidr=10.244.0.0/16 >> ~/kube-init.log"
    return cmd


# 获取init初始化后的kubeadm join token命令(与kubeInit函数绑定)
def joinToken():
    cmd = "cat ~/kube-init.log | grep -A1 'kubeadm join'"
    return cmd


# 获取kubeadm join token，token默认24小时过期(部署node及其他几套master需要)
def joinTokenNew():
    cmd = "sudo kubeadm token create --print-join-command > ~/kube-token.log;cat ~/kube-token.log | grep -A1 'kubeadm join'"
    return cmd


# 把获取到的token存放到文本内
def saveTokenFile(kube_join_cmd):
    with open(script_path + '/kube_join.csv', 'w+', newline='', encoding='utf-8') as out:
        csv_write = csv.writer(out, dialect='excel')
        dataList = [kube_join_cmd]
        csv_write.writerow(dataList)

# 拷贝pki文件
def pki():
    pass


# 把获取到的Token执行加入k8s集群
def joinMasterCluster():
    with open(script_path + '/kube_join.csv', 'r', newline='', encoding='utf-8') as out:
        csv_reader = csv.reader(out)
        cmd = ""
        for i in csv_reader:
            cmd += str(i)
        cmd = str(cmd).replace("[", "").replace("]", "").replace(",", ";").replace("'", "").replace("\"", "") + " --control-plane"
        return cmd

# 安装插件
def cniPlugin():
    cmd = "sudo kubectl --kubeconfig=//etc/kubernetes/admin.conf apply -f /tmp/*.yaml"
    return cmd

# 配置kubectl认证权限，使用
def kubectlPermission():
    cmd="mkdir -p $HOME/.kube && sudo yes|cp -rpf /etc/kubernetes/admin.conf $HOME/.kube/config && sudo chown $(id -u):$(id -g) $HOME/.kube/config && echo 'kubectl add home success' "
    return cmd



@app.task(name='dp_k8sMaster')
def dp_k8sMaster(host, port, username, password, advertise_address, deploy):
    print("master环境部署中......")
    ssh_remove_exec_cmd = sshChannelManager(host, port, username)
    cmd = yumKube()  # 部署
    ssh_remove_exec_cmd.sshExecCommand(cmd, password)
    cmd = cleanK8SRole() # 环境清理
    ssh_remove_exec_cmd.sshExecCommand(cmd, password)

    if deploy == 1:
        try:
            cmd = kubeInit(advertise_address)  # 初始化
            ssh_remove_exec_cmd.sshExecCommand(cmd, password)
            cmd = joinToken()  # 获取jointoken命令
            out = ssh_remove_exec_cmd.sshExecCommand(cmd, password)
            saveTokenFile(out)  # 存入本地
            cmd = kubectlPermission()  # 配置kubectl
            ssh_remove_exec_cmd.sshExecCommand(cmd, password)
            return {"code": 0, "message": "k8s master Init部署成功"}
        except Exception as e:
            return {"code": 1, "message": "k8s master Init部署失败原因+{status}".format(status=str(e))}

    elif deploy == 2:
        try:
            cmd = joinMasterCluster()  # 获取join token命令后执行加入
            out = ssh_remove_exec_cmd.sshExecCommand(cmd, password)
            saveTokenFile(out)
            cmd = kubectlPermission()  # 配置kubectl
            ssh_remove_exec_cmd.sshExecCommand(cmd, password)
            return {"code": 0, "message": "k8s join新master部署成功"}
        except Exception as e:
            print(e)
            return {"code": 1, "message": "k8s k8s join新master失败原因+{status}".format(status=str(e))}
