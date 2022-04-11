"""
"""
from django.http import JsonResponse
import json
from base.standard_respon import kmc_Response
from deploy_k8s_network_celery.tasks import dp_k8sNetwork


def k8sNetwork(request):
    """
    1.选择安装cni网络插件
    2.会根据cni_pulugin_yaml 目录下文件进行上传
    3.上传完毕会进行执行 yaml
    入参:
    ```
    http://0.0.0.0:8000/k8s_cni
    {
    "host":"192.168.1.202",
    "port":22,
    "username":"root",
    "password":"123456",
    "cni_name": "cilium"
     }
    ```
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
        pluginName = data.get('cni_name')
        pluginNameList = ["flannel", "cilium", "calico"]
        if pluginName in pluginNameList:
            if host and port and username and password and pluginName:
                task_id = dp_k8sNetwork.delay(pluginName, host, port, username, password)
                msg = "异步操作-安装网络 {cniName}插件.请跟进taskId进行查询结果....".format(cniName=pluginName)
                return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
        else:
            msg = "插件类型不支持,只支持" + ",".join(pluginNameList)
            return {"code": 1, "message": msg}
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
