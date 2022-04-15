from django.http import JsonResponse
import paramiko
import json
from deploy.base.standard_request import baseHttpApi
from django.conf import settings
import pprint
from deploy.base.standard_respon import kmc_Response


class k8sDeployCluster():
    def __init__(self, host, port, username, password):
        """
        1.初始化部署api接口参数
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def osUpgradeMain(self):
        """
        1..api方式调用内核升级业务功能
        """
        header = {'Content-Type': 'application/json'}
        payload = {"host": self.host, "port": self.port, "username": self.username, "password": self.password}
        HttpApi = baseHttpApi(method="post", url=settings.DEPLOY_OS_UPGRADE_API, header=header, body=payload)
        res = HttpApi.runMain()
        return res

    def k8sDeployBaseMain(self, hostname, ip):
        """
        1.api方式调用k8s部署 基础环境初始化
        """
        header = {'Content-Type': 'application/json'}
        payload = {"host": self.host, "port": self.port,
                   "username": self.username, "password": self.password,
                   "hostname": hostname, "ip": ip
                   }
        HttpApi = baseHttpApi(method="post", url=settings.DEPLOY_K8S_BASE_API, header=header, body=payload)
        res = HttpApi.runMain()
        pprint.pprint(res)
        return res

    def dockerServiceMain(self, log_size, registries):
        """
        1..api方式调用部署docker业务功能
        """
        header = {'Content-Type': 'application/json'}
        payload = {"host": self.host, "port": self.port,
                   "username": self.username, "password": self.password,
                   "log_size": log_size, "registries": registries
                   }
        HttpApi = baseHttpApi(method="post", url=settings.DEPLOY_DOCKER_API, header=header, body=payload)
        res = HttpApi.runMain()
        pprint.pprint(res)
        return res

    def k8sDeployMasterMain(self, deploy, ip):
        """
          1.api方式调用master部署init和K8S_Join master 业务功能
         """
        header = {'Content-Type': 'application/json'}
        payload = {"host": self.host, "port": self.port,
                   "username": self.username, "password": self.password,
                   "ip": ip,
                   "deploy": deploy
                   }
        HttpApi = baseHttpApi(method="post", url=settings.DEPLOY_K8S_MASTER_API, header=header, body=payload)
        res = HttpApi.runMain()
        pprint.pprint(res)
        return res

    def k8sDeployNetworkMain(self, cni_name="cilium"):
        """
        1.api方式调用部署k8s cni 网络插件业务功能
        """
        header = {'Content-Type': 'application/json'}
        payload = {"host": self.host, "port": self.port,
                   "username": self.username, "password": self.password,
                   "cni_name": cni_name
                   }
        HttpApi = baseHttpApi(method="post", url=settings.DEPLOY_K8S_NETWORK_API, header=header, body=payload)
        res = HttpApi.runMain()
        pprint.pprint(res)
        return res

    def k8sDeployNodeMain(self, api_server_ip=None, cluster_token=None, ca_cert_hash=None):
        """
        1.api方式调用部署k8s node环境部署功能
        """
        header = {'Content-Type': 'application/json'}
        payload = {"host": self.host, "port": self.port,
                   "username": self.username, "password": self.password,
                   "api_server_ip": ca_cert_hash,
                   "cluster_token": cluster_token,
                   "ca_cert_hash": ca_cert_hash
                   }
        HttpApi = baseHttpApi(method="post", url=settings.DEPLOY_K8S_NODE_API, header=header, body=payload)
        res = HttpApi.runMain()
        pprint.pprint(res)
        return res


def resourceSys():
    """
    1.感觉没有必要去实现.--
    """
    print("返回服务基本信息")
    data = {}
    df = server_resource.df(ssh_client)
    cpu = server_resource.cpu(ssh_client)
    mem = server_resource.mem(ssh_client)
    data["code"] = 0
    data["messgae"] = "k8s v1.23.5 version deploy success"
    data["Disk"] = df
    data["Cpu"] = cpu
    data["Mem"] = mem
    print(data)
    ssh_client.close()
    return data


def k8sDeploy(request):
    methodResponseMsg = """{method} Method not supported""".format(method=request.method)
    if request.method == "GET":
        return JsonResponse(kmc_Response(methodResponseMsg))
    elif request.method == "POST":
        data = json.loads(request.body)
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        hostname = data.get('hostname')
        ip = data.get('ip')  # master 以及 apiserver的ip
        log_size = data.get('log_size')
        registries = data.get('registries')
        cni_name = data.get('cni_name')
        deploy = data.get('deploy')
        k8s_instance = k8sDeployCluster(host=host, port=port, username=username, password=password)
        if deploy != 1:  # 这里接收master的ip、用户名及密码
            k8s_instance.k8sDeployMasterMain(deploy, ip)
            if deploy == 2:  # 执行拷贝master节点pki命令
                pass
        if deploy == 1 or deploy == 2 or deploy == 3:
            """
            # 内核升级-基础配置-Docker 环境部署(1、2、3都走)
            """
            print("系统内核升级中......")
            k8s_instance.osUpgradeMain()

            print("系统基本配置及参数优化中......")
            k8s_instance.k8sDeployBaseMain(hostname, ip)

            print("docker环境部署中......")
            k8s_instance.dockerServiceMain(log_size, registries)

        if deploy == 1 or deploy == 2:
            """
            # 安装master(deploy：1为需要init，deploy：2为加入master节点)
            """
            print("master环境部署中......")
            k8s_instance.k8sDeployMasterMain(deploy,ip)
            k8s_instance.k8sDeployNetworkMain(cni_name)

        if deploy == 3:
            """
            # 安装node(deploy：3为node节点)
            """
            k8s_instance.k8sDeployNodeMain()
        return JsonResponse(data)
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
