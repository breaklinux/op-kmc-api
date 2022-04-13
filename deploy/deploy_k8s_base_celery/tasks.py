import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_k8s_base_celery")  # 获取当前path路径
base = os.path.join(HOME_DIR, "base")
os.sys.path.append(script_path)
os.sys.path.append(base)

# 系统级别基础配置

import csv
from datetime_tools import runTime, runTimeCalculate
from ssh_channel import sshChannelManager
from main import app

# 配置K8Syum源
def aliK8sMirror():
    cmd = '''
    sudo cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
    '''
    return cmd


# 防火墙、selinux
def stopSecurity():
    cmd = "sudo sed -i 's/enforcing/disabled/' /etc/selinux/config;sudo setenforce 0;sudo systemctl stop firewalld;sudo systemctl disable firewalld"
    return cmd


# swap关闭
def stopSwap():
    cmd = "sudo swapoff -a;sudo sed -ri 's/.*swap.*/#&/' /etc/fstab"
    return cmd


# 配置主机名
def setHost(hostname):
    cmd = "sudo hostnamectl set-hostname {0}".format(hostname)
    return cmd


# 获取主机名及IP地址，存入到文本
def saveFile(hostname, ip):
    try:
        with open(script_path + '/hosts.csv', 'r+', newline='', encoding='utf-8') as out:
            csv_reader = csv.reader(out)
            hosts_list = []
            for i in csv_reader:
                if hostname == i[0] or ip == i[1]:
                    hosts_list.append(i[0])
                else:
                    with open(script_path + '/hosts.csv', 'a+', newline='', encoding='utf-8') as out:
                        csv_write = csv.writer(out, dialect='excel')
                        dataList = [hostname, ip]
                        csv_write.writerow(dataList)
    except Exception:
        with open(script_path + '/hosts.csv', 'w+', newline='', encoding='utf-8') as out:
            csv_write = csv.writer(out, dialect='excel')
            dataList = [hostname, ip]
            csv_write.writerow(dataList)


# 配置/etc/hosts,需要查文本
def setHosts():
    cmd = []
    with open(script_path + '/hosts.csv', 'r', newline='', encoding='utf-8') as out:
        csv_reader = csv.reader(out)
        for i in csv_reader:
            a = "sudo echo \"{0} {1}\" > /etc/hosts".format(i[1], i[0])
            cmd.append(a)
    cmd = str(cmd).replace("[", "").replace("]", "").replace(",", ";").replace("'", "")
    return cmd


# 设置时区
def setNtp():
    cmd = "sudo timedatectl set-timezone Asia/Shanghai;sudo timedatectl set-local-rtc 0;sudo systemctl restart rsyslog;sudo systemctl restart crond"
    return cmd


# 路由转发
def iptablesBridge():
    cmd = "sudo echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.d/k8s.conf;sudo echo 'net.bridge.bridge-nf-call-ip6tables = 1' >> /etc/sysctl.d/k8s.conf;sudo echo 'net.bridge.bridge-nf-call-iptables = 1' >> /etc/sysctl.d/k8s.conf"
    return cmd


# ipvs
def setIpvs():
    cmd = '''
    sudo cat > /etc/sysconfig/modules/ipvs.modules << EOF
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack
EOF
    sudo /bin/bash /etc/sysconfig/modules/ipvs.modules && lsmod | grep -e ip_vs -e nf_conntrack
    echo "/bin/bash /etc/sysconfig/modules/ipvs.modules" >>/etc/rc.local
    '''
    return cmd

# k8s 环境init初始化
@app.task(name='dp_k8sBase')
def dp_k8sBase(host, port, username, password, hostname):
    ssh_remove_exec_cmd = sshChannelManager(host, port, username)
    cmd = []
    cmd.append(saveFile(hostname,ip))
    cmd.append(aliK8sMirror())
    cmd.append(stopSecurity())
    cmd.append(stopSwap())
    cmd.append(setHost(hostname))
    cmd.append(setHosts())
    cmd.append(setNtp())
    cmd.append(iptablesBridge())
    cmd.append(setIpvs())
    print("k8s环境系统初始化中......")
    startInitTime = runTime()
    for init in cmd:
        ssh_remove_exec_cmd.sshExecCommand(init, password)
    endInitTime = runTime()
    runtime = runTimeCalculate("k8s环境系统初始化中耗时: ", endInitTime, startInitTime)
    return {"code": 0, "message": "k8s环境系统初始化成功", "runtime": str(runtime) + " s"}

