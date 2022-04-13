from django.http import JsonResponse
import json
from deploy.base.standard_respon import kmc_Response
from deploy.deploy_docker_service_celery.tasks import dp_dockerService


def dockerService(request):
    methodResponseMsg = """{method} Method not supported""".format(method=request.method)
    if request.method == "GET":
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
