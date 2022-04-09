# master安装
import csv


# 安装kubeadm、kubelet、kubectl，并设置开机自启
def yumKube():
    cmd = "sudo yum install -y kubelet-1.23.5-0 kubeadm-1.23.5-0 kubectl-1.23.5-0;sudo systemctl enable kubelet.service"
    return cmd


# kubeadm init 初始化(只有第一次部署master需要，需要参数deploy:1)，ip为kubeapi的地址
def kubeInit(ip):
    cmd = "sudo kubeadm init --v=5 --apiserver-advertise-address=" + str(
        ip) + " --image-repository registry.aliyuncs.com/google_containers --kubernetes-version v1.23.5 --service-cidr=10.1.0.0/16 --pod-network-cidr=10.244.0.0/16 > ~/kube-init.log"
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
    with open('./kube_join.csv', 'w+', newline='', encoding='utf-8') as out:
        csv_write = csv.writer(out, dialect='excel')
        dataList = [kube_join_cmd]
        csv_write.writerow(dataList)


# 拷贝pki文件
def pki():
    pass


# 把获取到的Token执行加入k8s集群
def joinMasterCluster():
    with open('./kube_join.csv', 'r', newline='', encoding='utf-8') as out:
        csv_reader = csv.reader(out)
        cmd = ""
        for i in csv_reader:
            cmd += str(i)
        cmd = str(cmd).replace("[", "").replace("]", "").replace(",", ";").replace("'", "").replace("\"", "") + " --control-plane"
        return cmd


# 配置kubectl认证权限，使用
def kubectlPermission():
    cmd = "mkdir -p $HOME/.kube;sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config;sudo chown $(id -u):$(id -g) $HOME/.kube/config"
    return cmd


# 部署flannel
def flannel():
    cmd = "kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml"
    return cmd
