#node安装
import csv

#安装kubelet、kubeadm
def yumKube():
    cmd="yum install -y kubelet-1.23.5-0 kubeadm-1.23.5-0;systemctl enable kubelet.service"
    return cmd

#把获取到的Token执行加入k8s集群(需要参数deploy:2)
def joinMasterCluster():
    with open('./kube_join.csv', 'r',newline='',encoding='utf-8') as out:
        csv_reader=csv.reader(out)
        cmd=""
        for i in csv_reader:
            cmd += str(i)
        cmd=str(cmd).replace("[","").replace("]","").replace(",",";").replace("'","")
        return cmd
