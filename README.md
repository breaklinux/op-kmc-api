# op-kmc-api
  
  1.kmc (Kubernetes Management Control ) K8S管理控制系统 本项目主要适用于开源版本K8S系统功能管理后台APi

# Contributing code person (贡献代码人员)

| Id | name | mail | things | used|
| --- | --- | --- | --- | --- |   
| 1   | breaklinux| breaklinux@163lcom |     |     |
|     |           |           |        |     |
|     |           |           |        |     |
|     |           |           |        |     |
|     |           |           |        |     |

# Requirement document (功能需求)

- 1.系统用户统一使用 LDAP 用户登录验证生成有时间限制Token 进行统一登录.
- 2.支持多版本开源K8S环境部署(部署Master + Node + Docker + nginx-Ingress + cni(网络插件)+ coreDns 至少 1 master + 2 node 以及添加在线添加Node节点功能
- 3.支持分支管理，确保最大化分支发布的自由度（支持选择应用的多个分支进行CI）-根据版本或者tags以及commit 进行CI构建镜像.
- 4.K8S常见资源管理(Deployment,Service,Ignress,Namespace,PV/PVC/StorageClass,Secret,StatefulSet,DaemonSet,CronJob,Job) 资源查询-创建-删除-修改
- 5.常规容器化发布(应用管理 → 应用配置 → 应用CI管理 → CD部署)
- 6.支持多语言发布(Java,Python,GO,Node) PHP可以暂不支持后期考虑 
- 7.发布回滚(基于镜像tag进行发布版本回滚-最大化只支持5个近期版本)
- 8.服务管理(根据命名空间纬度 查询-停止-启动-删除 POD等日常操作
- 9.CICD 发布通知支持 配置钉钉webhook 或者飞书IMA webhook.
- 10.K8S高级配置亲和性和反亲和探活接口配置
- 11.支持设置污点容忍和node标签指定调度.
- 12.发布人员进行关联 发布统计.参考月,周.日等纬度进行统计发布次数成功率. 

# 对接前端统一标准接口参数

**op-kmc-api 接口文档：** 
示例

-  LDAP登录验证接口

**请求URL：** 
- ` http://devops-op-kmc-api.com/api/v1/login`
  
**请求方式：**
- POST  

**格式：**  
- JSON  

**参数：** 

|参数   |必填   |类型   |说明   |
| ------------  | ------------ | ------------ | ------------ |
| username    |是   |str   |登录用户只支持单个LDAP用户名称
| password    |是   |str   |登录密码只支持单个LDAP用户密码
| type        |是   |str   |账号类型 默认值:ldap 或者 标准standard


 **请求示例**
```
{
	 "username":"ops",
	 "password":"123456789",
	 "type": "ldap"
}
```
 **标准正常返回参数**
```
{
   {
    "code": 0,
    "message": "登录正常",
    "data": {
        "token":"eyJhbGciOiJIUzI1NiIsInR5cCIU2cem9iZa2DVYNbTnL7u91Mpxxxx", #账号验证通过生成token 
        "state": true
    }
}
}
```
**标准错误返回参数**
```
{
   "code": 1,
   "message": "LDAP系统验证账号密码失败",
   "data": {  
        "token": "", 
        "state": false
    }
}
```

 **备注** 

- code状态码描述
  0 表示系统正常响应;
  1 表示系统内部出现问题;  

标准接口格式
```
{
  "code": 0 0或者1 固定
  "message": "业务消息"
  "data": {
   "自定义key": "自定义value"
   }
}
```
# 接口格式统一Result API 标准
```

 1.统一JSON数据格式返回:
    GET  查询资源 参数放在: Query Params key=value 查询
    POST 新增资源 参数放在body体中 
    PUT  更新资源 参数放在body体中带上资源id 和更新字段
    DELETE 删除资源 参数放在body体中 带上资源id 

```
    
# 接口安全
```
 1. 全部访问任何系统API资源都需要在 HTTP 中 Headers 携带token进行验证 除了LDAP用户认证生成token接口
```

2.  CURL 格式如下
 ```
curl --location --request GET 'https://devops-op-kmc-api.com/api/v1/getPods?page=1&page_size=10' \
--header 'Authorization: Bearer Basic xxxxGZnI3JkSWZYRDZab1o3YUJOdlk=' \
--data-raw ''
 
 ```
 
3. python 示例代码 方式
```
import requests

url = "https://devops-op-kmc-api.com/api/v1/?page=1&page_size=10"

payload = ""
headers = {
  'Authorization': 'Bearer Basic xxxxGZnI3JkSWZYRDZab1o3YUJOdlk='
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
```









