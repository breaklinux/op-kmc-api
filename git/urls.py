from django.urls import path,re_path
from .views import *

urlpatterns = [
    # 上传文件下载文件功能(独立与其他)
    path('prject' ,project),
    path('clone' ,clone),
]

'''
http://127.0.0.1:8000/gitlab/prject       POST
{
    # "url":"http://192.168.89.168/",
    # "token":"zyyg382EbfNJyDzwbyes",
    "project_name":"test"
}
---
http://127.0.0.1:8000/gitlab/clone       POST
{
    "http_url_to_repo":"http://192.168.89.168/root/test.git",
    "project_branch":"master", 或者 "project_tags":"master2",  只接其一参数
    "project_name":"test",
    # "token":"zyyg382EbfNJyDzwbyes",
}

'''