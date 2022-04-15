import requests
import pprint
import json

class baseHttpApi():
    """
    1.初始化参数
    """
    def __init__(self, method, url, header=None, body=None, timeout=300):
        self.url = url
        self.header = header
        self.body = body
        self.timeout = timeout
        self.method = method
    """
    1.封装公共 requests 发送请求实现CRUD
    2.支持GTE,POST,PUT,DELETE
    """

    def sendGet(self):
        """
          1.get 方法返回json
          2.不是json 直接返回
        """
        response = requests.get(url=self.url, headers=self.header, params=self.body, timeout=self.timeout)
        try:
            return response.json()
        except Exception as e:
            return response
        finally:
            response.close()

    def ifHeaderContentType(self):
        """        1.判断Header数据类型dict 和 body 也是dict
        """
        if type(self.header) is dict and type(self.body) is dict:
            if self.header['Content-Type'] == 'application/json':
                body = json.dumps(self.body)
            elif self.header['Content-Type'] == 'application/x-www-form-urlencoded':
                body = self.body
            else:
                body = ""
            return {"code": 0, "body": body, "status": "success"}
        else:
            return {"code": 1, "msg": "header头部体错误,请更改header体为字典典类型", "status": "failure"}

    def sendPost(self):
        """
        1.body 传入的请求体为字典类型.发送请、post请求
        2.header 类型只支持json 和x-www-form-urlencoded
        """
        result = self.ifHeaderContentType()
        if not result.get("body") is None:
            print(self.url)
            response = requests.post(url=self.url, headers=self.header, json=self.body, timeout=self.timeout)
            try:
                return response.json()
            except Exception as e:
                print(str(e))
                return response
        else:
            return result

    def sendPut(self):
        """
        1.公共 修改数据方法
        """
        result = self.ifHeaderContentType()
        if not result.get("body") is None:
            response = requests.post(url=self.url, headers=self.header, json=self.body, timeout=self.timeout)
            try:
                return response.json()
            except Exception as e:
                return response
            finally:
                response.close()
        else:
            return result

    def sendDelete(self):
        """
        1.请求删除方法
        2.判断类型
        3.返回结果
        """
        result = self.ifHeaderContentType()
        if not result.get("body") is None:
            response = requests.delete(url=self.url, headers=self.header, json=self.body, timeout=self.timeout)
            try:
                return response.json()
            except Exception as e:
                return response
            finally:
                response.close()
        else:
            return result

    def runMain(self):
        """
        1.请求方法类型 参数判断入口
        """
        if self.method == 'get':
            return self.sendGet()
        elif self.method == 'post':
            return self.sendPost()
        elif self.method == 'delete':
            return self.sendDelete()
        elif self.method == 'put':
            return self.sendPut()
        else:
            print({'code': '请求方法错误，请使用get/post/delete/put'})
            return {'code': '请求方法错误，请使用get/post/delete/put'}


# if __name__ == '__main__':
#     url = 'http://0.0.0.0:8000/k8s_init'
#     header = {'Content-Type': 'application/json'}
#     payload = {"host": "192.168.1.202", "port": 22, "username": "root", "password": "123456", "hostname": "master"}
#     method = "get"
#     HttpApi = baseHttpApi(method=method, url=url, header=header, body=payload)
#     res = HttpApi.runMain()
#     pprint.pprint(res)  # print()采用分行打印输出
#     # payload = {"host": "192.168.1.202", "port": 22, "username": "root", "password": "123456", "hostname": "master"}
#     # res = HttpApi.runMain('post', url='http://0.0.0.0:8000/k8s_init', header=header, body=payload, )
#     # pprint.pprint(res)
