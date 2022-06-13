# Generated by Django 3.2.13 on 2022-06-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dj_ldap_user',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_user', models.CharField(default='sys', max_length=128, verbose_name='创建人')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否在线')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('last_modified_user', models.CharField(default='sys', max_length=128, verbose_name='最后修改人')),
                ('username', models.CharField(max_length=128, verbose_name='用户名称')),
                ('user_id', models.CharField(max_length=32, verbose_name='用户id')),
                ('token', models.CharField(max_length=3096, verbose_name='用户token')),
                ('token_expired', models.CharField(max_length=64, verbose_name='用户token过期时间')),
            ],
            options={
                'db_table': 'ldap_user',
            },
        ),
    ]