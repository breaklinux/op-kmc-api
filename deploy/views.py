from django.http import JsonResponse
import paramiko
import json
from deploy.base.standard_request import baseHttpApi
from django.conf import settings
import pprint
from deploy.base.standard_respon import kmc_Response
import datetime


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

    def getIdMain(self, taskId):
        """
        1.api方式查询内核升级状态
       """
        header = {'Content-Type': 'application/json'}
        payload = {"task_id": taskId}
        HttpApi = baseHttpApi(method="get", url=settings.DEPLOY_OS_UPGRADE_API, header=header, body=payload)
        res = HttpApi.sendGet()
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


def k8sDeploy(request):
    """
    1.获取api参数进行部署k8s主逻辑
    2.部署过程20分钟如果没有完成终止 部署过程
    3.通过各个模块api访问调用处理.
    """
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
            endTime = datetime.datetime.now() + datetime.timedelta(minutes=10)
            resultTaskId = k8s_instance.osUpgradeMain()
            if resultTaskId.get("code") == 0 and resultTaskId.get("task_id"):
                while True:
                    resultCeleryStatus = k8s_instance.getIdMain(resultTaskId.get("task_id"))
                    if resultCeleryStatus['code'] == 0:
                        print('os内核升级成功--下一步进行k8s基础环境初始化', resultCeleryStatus)
                        break
                    else:
                        print('os内核升级还在处理中-循环查询状态中请稍后....10分钟无响应操作失败')
                        if datetime.datetime.now() >= endTime:
                            msg = "系统内核升级失败--10分钟没有完成.请升级机器配置或者检查原因"
                            return JsonResponse({"code": 1, "msg": msg})
            else:
                msg = "系统内核升级Api操作异常请进行检查....."
                return JsonResponse({"code": 1, "msg": msg})

            print("系统基本配置及参数优化中......")
            baseEndTime = datetime.datetime.now() + datetime.timedelta(seconds=15)
            resultBaseTaskId = k8s_instance.k8sDeployBaseMain(hostname, ip)
            print("k8s系统基础配置返回值", resultBaseTaskId)
            if resultBaseTaskId.get("code") == 0 and resultBaseTaskId.get("task_id"):
                while True:
                    resultBaseCeleryStatus = k8s_instance.getIdMain(resultBaseTaskId.get("task_id"))
                    if resultBaseCeleryStatus['code'] == 0:
                        print('k8s基础环境初始化--下一步进行Docker服务部署', resultBaseCeleryStatus)
                        break
                    else:
                        print('k8s基础环境初始化-循环查询状态中请稍后....15秒无响应操作失败')
                        if datetime.datetime.now() >= baseEndTime:
                            msg = "k8s基础环境初始化--15秒没有完成.请升级机器配置或者检查具体原因"
                            return JsonResponse({"code": 1, "msg": msg})
            else:
                msg = "k8s基础环境初始化异常请进行检查....."
                return JsonResponse({"code": 1, "msg": msg})

            return JsonResponse({"code": 1, "msg": "断点调试k8s基础环境初始化"})

            print("docker环境部署中......")
            dockerEndTime = datetime.datetime.now() + datetime.timedelta(minutes=8)

            resultDockerTaskId = k8s_instance.dockerServiceMain(log_size, registries)
            print("docker环境基础配置返回值", resultDockerTaskId)
            if resultDockerTaskId.get("code") == 0 and resultDockerTaskId.get("task_id"):
                while True:
                    resultDockerCeleryStatus = k8s_instance.getIdMain(resultDockerTaskId.get("task_id"))
                    if resultDockerCeleryStatus['code'] == 0:
                        print('k8s Docker环境部署成功--下一步进行Master Init', resultDockerCeleryStatus)
                        break
                    else:
                        print('k8s  Docker环境部署成功-循环查询状态中请稍后....8分钟无响应操作失败')
                        if datetime.datetime.now() >= dockerEndTime:
                            msg = "k8s Docker环境部失败--8分钟没有完成.请升级机器配置或者检查具体原因"
                            return JsonResponse({"code": 1, "msg": msg})
            else:
                msg = "k8s Docker环境部署异常请进行检查....."
                return JsonResponse({"code": 1, "msg": msg})

            return JsonResponse({"code": 1, "msg": "断点调试k8sDocker部署"})

        if deploy == 1 or deploy == 2:
            """
            # 安装master(deploy：1为需要init，deploy：2为加入master节点)
            """
            print("master环境部署中......")
            k8s_instance.k8sDeployMasterMain(deploy, ip)
            k8s_instance.k8sDeployNetworkMain(cni_name)

        if deploy == 3:
            """
            # 安装node(deploy：3为node节点)
            """
            k8s_instance.k8sDeployNodeMain()
        return JsonResponse(data)
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
