
def remoteHostScp(host_ip, remote_path, local_path, username,  password, port):
    t = paramiko.Transport((host_ip, port))
    t.connect(username=username, password=password) # 登录远程服务器
    sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
    src = remote_path
    des = local_path
    sftp.get(src,des)
    t.close()






def pluginListManager(pluginName):
    pluginNameList = ["flannel", "cilium", "calico"]
    if pluginName in pluginNameList:
        if pluginName == "flannel":
            cmd = "kubectl apply -f ./Flannel/kube-flannel.yaml"
        elif pluginName == "cilium":
            cmd = "kubectl apply -f ./Cilium/quick-install.yaml"
        else:
            cmd = "kubectl apply -f ./Flannel/rbac-kdd.yaml && kubectl apply -f ./kube_calico.yam"
        return cmd
    else:
        msg = "插件类型不支持,只支持" + ",".join(pluginNameList)
        return {"code": 1, "message": msg}



