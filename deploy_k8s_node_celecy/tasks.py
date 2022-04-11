# node安装
import csv
from deploy_k8s_base_celery.main import app

# 安装kubelet、kubeadm
def yumKube():
    cmd = "sudo yum install -y kubelet-1.23.5-0 kubeadm-1.23.5-0;systemctl enable kubelet.service"
    return cmd

# 把获取到的Token执行加入k8s集群(需要参数deploy:2)
def joinMasterCluster():
    with open('./kube_join.csv', 'r', newline='', encoding='utf-8') as out:
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
    cmd_list.append(joinNodeToasterCluster(apiServerIp, token, caCertHash))
    for node in cmd_list:
        ssh_remove_exec_cmd.sshExecCommand(node, password)
