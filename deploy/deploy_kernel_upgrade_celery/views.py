
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
            task_id = dp_upgradeKernel.delay(host, port, username, password)
            msg = "异步操作-更新os系统内核中.请跟进taskId进行查询结果...."
            return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))

