import logging
import os
import time
from celery_tasks.main import app
import paramiko
from django.http import JsonResponse
#from tools.datetime_tools import runTime, runTimeCalculate

# 升级操作系统内核版本.便于后期新增组件和ebpf cni插件功能
import csv


# 升级操作系统最新软件包
def updateYum():
    cmd = "sudo yum -y update "
    return cmd


# 获取升级内核yum源
def changeKernelRepo():
    cmd = "sudo rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org && rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm"
    return cmd


# 查看所有kernel新版本..
def list_kernel():
    cmd = "sudo yum --disablerepo='*' --enablerepo='elrepo-kernel' list available"
    return cmd


# 安装kernel-ml 新.版本.
def installNewKernel():
    cmd = "sudo yum -y --enablerepo=elrepo-kernel install kernel-ml"
    return cmd


# 查看可用内核
def listNewKernels():
    cmd = '''sudo awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg'''
    return cmd

# 安装ipvs软件包

def installIpvsPkg():
    cmd = "sudo yum -y install ipset ipvsadm"
    return cmd

# 设置内核启动
def setGrubBot():
    cmd = '''sudo 
    grub2-set-default 0 '''
    return cmd

# 生成grub文件
def buildGrub():
    cmd = "sudo grub2-mkconfig -o /boot/grub2/grub.cfg"
    return cmd

# 重启机器...
def rebootSystem(is_boot=False):
    if is_boot:
        cmd = "sudo reboot"
        return cmd
    else:
        print("host reboot")

# 查看内核版本
def listKernelRpm():
    cmd = "sudo rpm -qa | grep kernel"
    return cmd

# 卸载旧版本内核
def uninstallOldKernel():
    cmd = "sudo yum remove -y kernel-tools-libs-3.*  kernel-3.* "
    return cmd

# 安装utils工具
def installYumUtils():
    cmd = "sudo yum install -y yum-utils"
    return cmd

# 新内核补丁mpt2sas升级为mpt3sas
def mpt2sasToMpt3sas():
    cmd = "dracut --force --add-drivers mpt3sas --kver=5.3.6"
    return cmd

# 删除旧版本
"""
uninstall_old_packages() {
    uninstall_old_kernel
    install_yum_utils
    echo -e "\033[32m 删除旧版本包... \033[0m"
    package-cleanup --oldkernels -y
}
"""



def sshCmd(ssh_client, c):
    print("执行命令:{0}".format(c))
    stdin, stdout, stderr = ssh_client.exec_command(c, get_pty=True)
    if not stdout is None:
        data = stdout.read()
        data = data.decode("utf-8")
        print("命令执行结果：" + str(data))
        return data
    if not stderr is None:
        data = stderr.read()
        data = data.decode("utf-8")
        print("命令执行错误：" + str(data))
        return data.read()

def sshLinux(host, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    return ssh_client

# 升级内核主入口
@app.task(name='upgradeKernel')
def upgradeKernel(host, port, username, password):
    cmd = []
    cmd.append(updateYum())
    cmd.append(changeKernelRepo())
    cmd.append(installIpvsPkg())
    cmd.append(list_kernel())
    cmd.append(installNewKernel())
    cmd.append(buildGrub())
    cmd.append(rebootSystem())
    cmd.append(listNewKernels())
    cmd.append(uninstallOldKernel())
    print("操作系统内核更新升级中......")
    #startUpgradeTime = runTime()
    for upgrade in cmd:
        sshCmd(sshLinux(host, port, username, password),upgrade)
    #endUpgradeTime = runTime()
    #runTimeCalculate("操作系统内核更新升级中耗时: ", endUpgradeTime, startUpgradeTime)

