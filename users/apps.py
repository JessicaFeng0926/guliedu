from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    #在这里取一个verbose_name，在站点就会以中文显示app的名字
    verbose_name='用户模块'
