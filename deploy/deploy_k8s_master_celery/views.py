"""
"""
from django.http import JsonResponse
import json
from deploy.base.standard_respon import kmc_Response
from deploy.deploy_k8s_master_celery.tasks import dp_k8sMaster


def k8sMaster(request):
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
        advertise_address = data.get('ip')
        deploy = data.get('deploy')
        deployLit = [1, 2]
        if deploy in deployLit:
            if host and port and username and password and advertise_address:
                task_id = dp_k8sMaster.delay(host, port, username, password, advertise_address, deploy)
                if deploy == 1:
                    msg = "异步操作-K8S_Init.请跟进taskId进行查询结果...."
                else:
                    msg = "异步操作-K8S_Join.请跟进taskId进行查询结果...."
                return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
        else:
            msg = "输入类型k8S不支持..支持1 和 2(k8s init初始化,2 k8s join加入节点)"
            return JsonResponse(kmc_Response(msg=msg))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
