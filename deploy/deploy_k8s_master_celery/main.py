import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "deploy_k8s_master_celery")  # 获取当前path路径
os.sys.path.append(script_path)

from celery import Celery
import config

# 创建celery应用
app = Celery('dp_k8s_master')

# 导入celery配置
app.config_from_object(config)

# 自动注册celery任务
# 在指定的包中找tasks.py文件，在这个文件中找@app.task的函数，当做任务
# app.autodiscover_tasks()  # 自动

# 定时任务需要添加
app.autodiscover_tasks(['deploy_k8s_master_celery.base_info'])
# # 在出现worker接受到的message出现没有注册的错误时，使用下面一句能解决
imports = ("tasks",)
