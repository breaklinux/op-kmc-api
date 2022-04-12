# 部署docker

import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_docker_service_celery")  # 获取当前path路径
base = os.path.join(HOME_DIR, "base")
os.sys.path.append(script_path)
os.sys.path.append(base)

from datetime_tools import runTime, runTimeCalculate
from ssh_channel import sshChannelManager
from .main import app


# 安装依赖包
def dependentPackages():
    cmd = "sudo sed -i 's/enabled=1/enabled=0/g' /etc/yum/pluginconf.d/fastestmirror.conf && sudo sed -i 's/plugins=1/plugins=0/g' /etc/yum.conf && sudo yum -y install yum-utils device-mapper-persistent-data lvm2 && sudo yum clean all "
    return cmd


# 设置阿里云repo仓库
def aliDockerMirror():
    cmd = "sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo"
    return cmd


# 安装docker服务
def yumDocker():
    cmd = "sudo yum -y install docker-ce"
    return cmd


# 配置daemon(需要传递日志容量及仓库地址)
def daemon(logsize, registries):
    cmd = '''
    sudo mkdir /etc/docker;
    sudo mkdir -p /etc/systemd/system/docker.service.d;
    sudo cat > /etc/docker/daemon.json << EOF
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts":{
        "max-size": "''' + str(logsize) + '''"
    },
    "insecure-registries": ["''' + str(registries) + '''"],
    "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
    '''
    return cmd


# 服务重新加载
def reload():
    cmd = "sudo systemctl daemon-reload;sudo systemctl restart docker;sudo systemctl enable docker"
    return cmd


@app.task(name='dp_dockerService')
def dp_dockerService(host, port, username, password, logsize, registries):
    ssh_remove_exec_cmd = sshChannelManager(host, port, username)
    cmd = []
    cmd.append(dependentPackages())
    cmd.append(aliDockerMirror())
    cmd.append(yumDocker())
    cmd.append(daemon(logsize, registries))
    cmd.append(reload())
    print("k8s Docker服务部署中......")
    startInitTime = runTime()
    for docker in cmd:
        ssh_remove_exec_cmd.sshExecCommand(docker, password)
    endInitTime = runTime()
    runtime = runTimeCalculate("k8s Docker服务部署中耗时: ", endInitTime, startInitTime)
    return {"code": 0, "message": "k8s Docker服务部署成功", "runtime": str(runtime) + " s"}
