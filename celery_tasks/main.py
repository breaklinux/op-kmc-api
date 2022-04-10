import os
import logging
from datetime import timedelta
from celery import Celery
from celery_tasks import config

# 创建celery应用
app = Celery('upgradeKernel', broker="redis://192.168.1.202:6379/0",backend="redis://192.168.1.202:6379/1")

# 导入celery配置
app.config_from_object(config)

# 自动注册celery任务
# 在指定的包中找tasks.py文件，在这个文件中找@app.task的函数，当做任务
# app.autodiscover_tasks()  # 自动

# 定时任务需要添加
app.autodiscover_tasks(['celery_tasks.base_info'])
# # 在出现worker接受到的message出现没有注册的错误时，使用下面一句能解决
imports = ("tasks",)
