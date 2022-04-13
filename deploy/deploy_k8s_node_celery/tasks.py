import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]

script_path = os.path.join(HOME_DIR, "deploy_k8s_node_celery")  # 获取当前path路径
os.sys.path.append(script_path)

base = os.path.join(HOME_DIR, "base")
os.sys.path.append(base)

master_token_path = os.path.join(HOME_DIR, "deploy_k8s_node_celery")  # 获取当前Master目录下路径
os.sys.path.append(master_token_path)

# node安装
import csv
from .main import app
from datetime_tools import runTime, runTimeCalculate
from ssh_channel import sshChannelManager


# 安装kubelet、kubeadm
def yumKube():
    cmd = "sudo yum install -y kubelet-1.23.5-0 kubeadm-1.23.5-0;systemctl enable kubelet.service"
    return cmd


# 把获取到的Token执行加入k8s集群(需要参数deploy:2)
def joinMasterCluster():
    with open(master_token_path + '/kube_join.csv', 'r', newline='', encoding='utf-8') as out:
        csv_reader = csv.reader(out)
        cmd = ""
        for i in csv_reader:
            cmd += str(i)
        cmd = str(cmd).replace("[", "").replace("]", "").replace(",", ";").replace("'", "")
        return cmd


# 传递token 和 认证信息
def joinNodeToasterCluster(apiServerIp, token, caCertHash):
    cmd = "kubeadm join {apiServerIp}:6443 --token {token} \
    --discovery-token-ca-cert-hash {token}".format(
        ip=apiServerIp, token=token, ca_cert_hash=caCertHash)
    return cmd


@app.task(name='dp_k8sNode')
def dp_k8sNode(host, port, username, password, apiServerIp, token, caCertHash):
    ssh_remove_exec_cmd = sshChannelManager(host, port, username)
    # 安装node(deploy：3为node节点)
    print("node环境部署中......")
    cmd_list = []
    cmd_list.append(yumKube())
    if apiServerIp and token and caCertHash:
        cmd_list.append(joinNodeToasterCluster(apiServerIp, token, caCertHash))
        for node in cmd_list:
            ssh_remove_exec_cmd.sshExecCommand(node, password)
    else:
        cmd_list.append(joinMasterCluster())
        for node in cmd_list:
            ssh_remove_exec_cmd.sshExecCommand(node, password)
