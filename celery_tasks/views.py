from deploy import os_kernel_upgrade, base, docker, master, node, server_resource
from django.http import JsonResponse
import json
from celery_tasks.base_info.tasks import upgradeKernel


def kernelUpgrade(request):
    methodResponseMsg = """{method} Method not supported""".format(method=request.method)
    if request.method == "GET":
       return JsonResponse(standardResponse(methodResponseMsg))
    elif request.method == "POST":
        data = json.loads(request.body)
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        if host and port and username and password:
            task_id = upgradeKernel.delay(host, port, username, password)
            msg = "异步操作-更新os系统内核中.请跟进taskId进行查询结果...."
            return JsonResponse(standardResponse(msg=msg, taskId=task_id))
    else:
        return JsonResponse(standardResponse(methodResponseMsg))


"""
 1.公共返回数据格式
"""


def standardResponse(msg=None, token=None, taskId=None):
    if not token:
        data = {"code": 1, "message": msg, "data": {"token": "", "state": "false"}, "task_id": str(taskId)}
    else:
        data = {"code": 0, "message": msg, "data": {"token": token, "state": "true"}, "task_id": str(taskId)}
    return data
