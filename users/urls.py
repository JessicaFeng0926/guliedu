from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^user_register/$',views.user_register,name='user_register'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
    re_path(r'^user_logout/$',views.user_logout,name='user_logout'),
    #下面这个路由是用来做用户激活的，它需要接收一个验证码，所以正则用\w+
    re_path(r'^user_active/(\w+)/$',views.user_active,name='user_active'),
    #下面是忘记密码的路由
    re_path(r'^user_forget/$',views.user_forget,name='user_forget'),
    #下面是修改密码的路由
    re_path(r'^user_reset/(\w+)/$',views.user_reset,name='user_reset'),
]