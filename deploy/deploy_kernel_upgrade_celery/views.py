import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_kernel_upgrade_celery")  # 获取当前path路径
base = os.path.join(HOME_DIR, "base")
os.sys.path.append(script_path)
os.sys.path.append(base)

from django.http import JsonResponse
import json
from deploy.deploy_kernel_upgrade_celery.tasks import dp_upgradeKernel
from standard_respon import kmc_Response
from celery.result import AsyncResult
from .main import app


def kernelUpgrade(request):
    """
    1.查询内核更新异步状态需要id
    2.开始异步更新
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
                msg = "更新系统内核任务还在等待队列中......"
                return JsonResponse({"code": 1, "msg": msg})
            elif async_result.failed():
                msg = "更新系统内核任务执行失败......"
                return JsonResponse({"code": 1, "msg": msg})
            elif async_result.status == 'RETRY':
                msg = "更新系统内核异常后正在重试....."
                return JsonResponse({"code": 1, "msg": msg})
            elif async_result.status == 'STARTED':
                msg = '更新系统内核已经开始执行执行中....'
                return JsonResponse({"code": 1, "msg": msg})
        else:
            methodResponseMsg = "没有任务task_id,不能进行操作"
            return JsonResponse({"code": 1, "msg": methodResponseMsg})
        return JsonResponse({"code": 1, "msg": methodResponseMsg})

    elif request.method == "POST":
        data = json.loads(request.body)
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        if host and port and username and password:
            print(data)
            msg = "异步操作-更新os系统内核中.请跟进taskId进行查询结果...."
            task_id = dp_upgradeKernel.delay(host, port, username, password)
            return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
