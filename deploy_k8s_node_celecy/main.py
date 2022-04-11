import os
import logging
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kmc.settings')
# 创建celery应用
app = Celery('dp_k8s_node')

# 导入celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动注册celery任务
# 在指定的包中找tasks.py文件，在这个文件中找@app.task的函数，当做任务
# app.autodiscover_tasks()  # 自动

# 定时任务需要添加
app.autodiscover_tasks(['deploy_k8s_node_celery.base_info'])
# # 在出现worker接受到的message出现没有注册的错误时，使用下面一句能解决
imports = ("tasks",)
