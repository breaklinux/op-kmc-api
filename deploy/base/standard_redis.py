from django.http import JsonResponse
from django_redis import get_redis_connection
from deploy.base.standard_respon import kmc_Response
redis_conn = get_redis_connection()

class getRedisManager():
    def stringGet(self, keyName):
        """
        #1.1.  String类型
        """
        if keyName:
            result_key = redis_conn.get(keyName).decode(encoding='utf-8')
            print(result_key)
            return JsonResponse()
        else:
            msg = "failure"
            return JsonResponse({"code": 1, "msg": msg})

    def listGet(self, keyName):
        """
        1. # list类型
        """
        return redis_conn.lpush('yy','123123')
