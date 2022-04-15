from django.http import JsonResponse
import json
from deploy.base.standard_respon import kmc_Response
from deploy.deploy_k8s_base_celery.tasks import dp_k8sBase

def k8sInit(request):
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
        hostname = data.get('hostname')
        ip = data.get("ip")
        print(data)
        if host and port and username and password and hostname:
            task_id = dp_k8sBase.delay(host, port, username, password, hostname, ip)
            msg = "异步操作-初始化.请跟进taskId进行查询结果...."
            return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))

