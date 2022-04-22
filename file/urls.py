from django.urls import path,re_path
from .views import *

urlpatterns = [
    # 上传文件下载文件功能(独立与其他)
    path('upload' ,upload),
    path('listfile' ,listfile),
    re_path('download/(?P<a1>\w+)' ,download)
]

'''
http://127.0.0.1:8000/file/upload   web GET访问
'''