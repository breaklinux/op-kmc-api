# Create your models here.
from django.db import models
# 定义基础数据类型
STRFTIME_FORMAT = "%Y-%m-%d %H:%M:%S"

"""
1.基类标准字段创建人.创建时间，修改时间,后修改人
"""

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_user = models.CharField(max_length=128, default="sys", verbose_name=u'创建人')
    is_active = models.BooleanField(default=True, verbose_name=u'是否在线')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=u'创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    last_modified_user = models.CharField(max_length=128, default="sys", verbose_name=u'最后修改人')

    class Meta:
        abstract = True


"""
1.ldap 用户信息表
2.return dict返回类型
"""

class dj_ldap_user(BaseModel):
    username = models.CharField(max_length=128, verbose_name="用户名称")
    user_id = models.CharField(max_length=32, verbose_name="用户id")
    token = models.CharField(max_length=3096, verbose_name="用户token")
    token_expired = models.CharField(max_length=64, verbose_name="用户token过期时间")

    class Meta:
        db_table = "ldap_user"

    def __str__(self):
        return str(self.id)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "user_id": self.upstreamname,
                "token": self.token}


