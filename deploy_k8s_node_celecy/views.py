"""
"""
from django.http import JsonResponse
import json
from base.standard_respon import kmc_Response
from deploy_k8s_node_celecy.tasks import dp_k8sNode


def k8sNode(request):
    methodResponseMsg = """{method} Method not supported""".format(method=request.method)
    if request.method == "GET":
        return JsonResponse(kmc_Response(methodResponseMsg))
    elif request.method == "POST":
        data = json.loads(request.body)
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        api_server_address = data.get('api_server_ip')
        cluster_token = data.get('cluster_token')
        caCertHash = data.get('ca_cert_hash')
        if host and port and username and password and api_server_address and cluster_token and caCertHash:
            task_id = dp_k8sNode.delay(host, port, username, password, api_server_address, cluster_token, caCertHash)
            msg = "异步操作-添加k8s_node节点.请跟进taskId进行查询结果...."
            return JsonResponse(kmc_Response(msg=msg, taskId=task_id))
        else:
            msg = "输入参数缺失..请检查后进行操作)"
            return JsonResponse(kmc_Response(msg=msg))
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))
