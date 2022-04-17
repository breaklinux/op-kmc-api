import os
HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_kernel_upgrade_celery")  # 获取当前path路径
base = os.path.join(HOME_DIR, "base")
os.sys.path.append(script_path)
os.sys.path.append(base)
from .main import app
from ssh_channel import sshChannelManager
app.autodiscover_tasks()
# 升级操作系统内核版本.便于后期新增组件和ebpf cni插件功能

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
    cmd = "grep 'menuentry' /etc/grub2.cfg |grep 'CentOS Linux'"
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
        cmd = "sudo rpm -qa | grep 'kernel-5.*'"
        return cmd


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


# 升级内核主入口
@app.task(name='dp_upgradeKernel')
def dp_upgradeKernel(host, port, username, password):
    ssh_remove_exec_cmd = sshChannelManager(host, port, username)
    cmd = []
    cmd.append(updateYum())
    cmd.append(changeKernelRepo())
    cmd.append(installIpvsPkg())
    cmd.append(list_kernel())
    cmd.append(installNewKernel())
    cmd.append(buildGrub())
    #cmd.append(rebootSystem())
    cmd.append(listNewKernels())
    #cmd.append(uninstallOldKernel())
    print("操作系统内核更新升级中......")
    try:
        for upgrade in cmd:
            ssh_remove_exec_cmd.sshExecCommand(upgrade, password)
        return {"code": 0, "message": "操作系统内核更新升级成功"}
    except Exception as e:
        return {"code": 1, "message": "操作系统内核更新失败原因+{status}".format(status=str(e))}
