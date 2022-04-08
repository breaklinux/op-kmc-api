#部署docker

#安装依赖包
def dependentPackages():
    cmd="sudo sed -i 's/enabled=1/enabled=0/g' /etc/yum/pluginconf.d/fastestmirror.conf && sudo sed -i 's/plugins=1/plugins=0/g' /etc/yum.conf && sudo yum -y install yum-utils device-mapper-persistent-data lvm2 && sudo yum clean all "
    return cmd

#设置阿里云repo仓库
def aliDockerMirror():
    cmd="sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo"
    return cmd

#安装docker服务
def yumDocker():
    cmd="yum -y update;sudo yum -y install docker-ce"
    return cmd

#配置daemon(需要传递日志容量及仓库地址)
def daemon(logsize,registries):
    cmd='''
    sudo mkdir /etc/docker;
    sudo mkdir -p /etc/systemd/system/docker.service.d;
    sudo cat > /etc/docker/daemon.json << EOF
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts":{
        "max-size": "'''+str(logsize)+'''"
    },
    "insecure-registries": ["'''+str(registries)+'''"],
    "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
    '''
    return cmd

#服务重新加载
def reload():
    cmd="sudo systemctl daemon-reload;sudo systemctl restart docker;sudo systemctl enable docker"
    return cmd

def deployDocker(logsize,registries):
    cmd=[]
    cmd.append(dependentPackages())
    cmd.append(aliDockerMirror())
    cmd.append(yumDocker())
    cmd.append(daemon(logsize,registries))
    cmd.append(reload())
    return cmd