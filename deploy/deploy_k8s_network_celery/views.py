"""
"""
from django.http import JsonResponse
import json
from deploy.base.standard_respon import kmc_Response
from deploy.deploy_k8s_network_celery.tasks import dp_k8sNetwork


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
        taskId = request.GET.get("task_id")
        if taskId:
            async_result = AsyncResult(id=taskId, app=app)
            if async_result.successful():
                result = async_result.get()
                result["data"] = {"token": "", "state": "true"}
                result["task_id"] = taskId
                return JsonResponse(result)
            elif async_result.status == 'PENDING':
                msg = "任务还在等待队列中......"
            elif async_result.failed():
                msg = "任务执行失败......"
            elif async_result.status == 'RETRY':
                msg = "任务异常后正在重试....."
            elif async_result.status == 'STARTED':
                msg = '任务已经开始执行执行中....'
            return JsonResponse({"code": 1, "msg": msg})
        else:
            methodResponseMsg = "没有任务task_id,不能进行操作"
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
