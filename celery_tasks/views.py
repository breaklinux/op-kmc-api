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
            a = upgradeKernel(host, port, username, password).delay()
            msg = "异步更新-更新os系统内核中....."
            return JsonResponse(standardResponse(msg))
    else:
        return JsonResponse(standardResponse(methodResponseMsg))


"""
 1.公共返回数据格式
"""


def standardResponse(msg=None, token=None):
    if not token:
        data = {"code": 1, "message": msg, "data": {"token": "", "state": "false"}}
    else:
        data = {"code": 0, "message": msg, "data": {"token": token, "state": "true"}}
    return data
