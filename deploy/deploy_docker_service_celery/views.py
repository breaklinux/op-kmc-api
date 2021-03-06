from django.http import JsonResponse
import json
from deploy.base.standard_respon import kmc_Response
from deploy.deploy_docker_service_celery.tasks import dp_dockerService


def dockerService(request):
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
                return JsonResponse({"code": 1, "msg": msg})

            elif async_result.failed():
                msg = "任务执行失败......"
                return JsonResponse({"code": 1, "msg": msg})
            elif async_result.status == 'RETRY':
                msg = "任务异常后正在重试....."
                return JsonResponse({"code": 1, "msg": msg})

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
        logSize = data.get('log_size')
        reg = data.get('registries')
        if host and port and username and password and logSize and reg:
            task_id = dp_dockerService.delay(host, port, username, password, logSize, reg)
            msg = "异步操作-Docker部署.请跟进taskId进行查询结果...."
            return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
        else:
            msg = "参数不足,请进行检查"
            return JsonResponse(kmc_Response(msg=msg))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
