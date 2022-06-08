from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import paramiko
import json
from deploy.base.standard_request import baseHttpApi
from django.conf import settings
import pprint
from deploy.base.standard_respon import kmc_Response
import datetime
from account.ldapApi import MyLdapOps, newLdap
from account.jwt_tool import *


def LdapAuth(request):
    methodResponseMsg = """{method} Method not supported""".format(method=request.method)
    if request.method == "GET":
        return JsonResponse(kmc_Response(methodResponseMsg))
    elif request.method == "POST":
        # instance = MyLdapOps()
        instance = newLdap()
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        resultData = instance.valid_user(
            data.get("username"),
            data.get('password')
        )
        print(resultData)
        if resultData.get("code") == 0:
            info = {"user_id": "10086"}
            token = gen_token(info)
            data = {"msg": "登录成功!", "token": token, "code": 0}
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"code": 50000, "message": resultData.get("message"),
                                 "data": {"token": "", "state": False, "user": resultData.get("user")}})
    else:
        return JsonResponse(kmc_Response(methodResponseMsg))


"""
1. 获取token
2.解析token获取用户身份信息
"""

def get_some_data(req):
    try:
        token = req.META["HTTP_TOKEN"]
        print(token)
    except Exception as e:
        pprint(e)
        return JsonResponse({"msg": "缺少token!"}, safe=False)
    res = jwt_tool.parser_token(token)
    if res["code"] == 1:
        user_id = res["data"]["user_id"]
        return JsonResponse({"msg": "您的id为:%s" % user_id, "data": "一些数据!"}, safe=False)
    else:
        return JsonResponse({"msg": "身份验证失败 请重新登录!"}, safe=False)


def LdapLogout():
    return JsonResponse({"code": 20000, "message": "ok"})
