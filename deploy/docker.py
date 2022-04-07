#部署docker

#安装依赖包
def dependentPackages():
    cmd="sudo yum -y install yum-utils device-mapper-persistent-data lvm2"
    return cmd

#设置阿里云repo仓库
def aliDockerMirror():
    cmd="sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo"
    return cmd

#安装docker服务
def yumDocker():
    cmd="sudo yum update -y && sudo yum install -y docker-ce"
    return cmd

#配置daemon(需要传递日志容量及仓库地址)
def daemon(logsize,registries):
    cmd='''
    sudo mkdir /etc/docker;
    sudo mkdir -p /etc/systemd/system/docker.service.d;
    sudo cat > /etc/docker/daemon.json << EOF
{
    #文件驱动，使用systemd进行文件隔离
    "exec-opts": ["native.cgroupdriver=systemd"],
    #日志机制
    "log-driver": "json-file",
    "log-opts":{
        #日志最大容量
        "max-size": "'''+str(logsize)+'''"
    },
    "insecure-registries": ["'''+str(registries)+'''"] 
}
EOF
    '''
    return cmd

#服务重新加载
def reload():
    cmd="sudo systemctl daemon-reload && sudo systemctl restart docker && sudo systemctl enable docker"
    return cmd

def deployDocker(logsize,registries):
    cmd=[]
    cmd.append(dependentPackages())
    cmd.append(aliDockerMirror())
    cmd.append(yumDocker)
    cmd.append(daemon(logsize,registries))
    cmd.append(reload())
    return cmd