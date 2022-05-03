from django.urls import path
from account.views import *
urlpatterns = [
    path('api/v1/', LdapAuth, name="登录验证")
]
