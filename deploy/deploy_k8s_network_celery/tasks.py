import os
HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_k8s_network_celery")  # 获取当前path路径
os.sys.path.append(script_path)
base = os.path.join(HOME_DIR, "base")
os.sys.path.append(script_path)
os.sys.path.append(base)

from main import app
from ssh_channel import sshChannelManager

@app.task(name='dp_k8sNetwork')
def dp_k8sNetwork(pluginName, host, port, username, passwd):
    """
    1.拷贝本地 cni yaml文件到服务器上
    2.执行kubectl apply -f 网络cni插件 yaml文件
    """
    scpChannel = sshChannelManager(host, port, username)
    if pluginName == "flannel":
        remote_path = "/tmp/kube-flannel.yaml"
        local_path = script_path + "/cni_plugin_yaml/Flannel/kube-flannel.yaml"
        result = scpChannel.remoteHostScp(passwd, local_path, remote_path)
        if result.get("msg") == "success":
            cmd = "kubectl apply -f {remote_filepath} ".format(remote_filepath=remote_path)
            scpChannel.sshExecCommand(cmd, passwd)
        else:
            return result.get("info")

    elif pluginName == "cilium":
        remote_path = "/tmp/quick-install.yaml"
        local_path = script_path + "/cni_plugin_yaml/Cilium/quick-install.yaml"
        scpChannel.remoteHostScp(passwd, local_path, remote_path)
        result = scpChannel.remoteHostScp(passwd, local_path, remote_path)
        print(result)
        # if result.get("msg") == "success":
        #     cmd = "kubectl apply -f {remote_filepath} ".format(remote_filepath=remote_path)
        #     scpChannel.sshExecCommand(cmd, passwd)
        #     print("执行文件")
        # else:
        #     return result.get("info")

    else:
        local_path = script_path + "/cni_plugin_yaml/Calico/kube_calico.yam"
        remote_path = "/tmp/kube_calico.yaml"
        scpChannel.remoteHostScp(passwd, local_path, remote_path)
        result = scpChannel.remoteHostScp(passwd, local_path, remote_path)
        if result.get("msg") == "success":
            cmd = "kubectl apply -f {remote_filepath} ".format(remote_filepath=remote_path)
            try:
                scpChannel.sshExecCommand(cmd, passwd)
                return {"code": 0, "message": "k8s网络插件部署成功"}
            except Exception as e:
                return {"code": 1, "message": "k8s网络插件部署失败+{status}".format(status=str(e))}
        else:
            return result.get("info")
