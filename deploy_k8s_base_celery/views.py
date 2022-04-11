from django.http import JsonResponse
import json
from base.standard_respon import kmc_Response
from deploy_k8s_base_celery.tasks import dp_k8sBase

def k8sInit(request):
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
        if host and port and username and password and hostname:
            task_id = dp_k8sBase.delay(host, port, username, password, hostname)
            msg = "异步操作-初始化.请跟进taskId进行查询结果...."
            return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))

