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

# 对接前端统一接口返回参数













