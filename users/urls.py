from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^user_register/$',views.user_register,name='user_register'),
    re_path(r'^user_login/$',views.UserLoginView.as_view(),name='user_login'),
    re_path(r'^user_logout/$',views.user_logout,name='user_logout'),
    #下面这个路由是用来做用户激活的，它需要接收一个验证码，所以正则用\w+
    re_path(r'^user_active/(\w+)/$',views.user_active,name='user_active'),
    #下面是忘记密码的路由
    re_path(r'^user_forget/$',views.user_forget,name='user_forget'),
    #下面是修改密码的路由
    re_path(r'^user_reset/(\w+)/$',views.user_reset,name='user_reset'),
    #下面是用户个人中心首页的路由
    re_path(r'^user_info/$',views.user_info,name='user_info'),
    #下面是用户个人中心上传头像的路由
    re_path(r'^user_changeimage/$',views.user_changeimage,name='user_changeimage'),
    #下面是用户个人中心修改普通信息的路由
    re_path(r'^user_changeinfo/$',views.user_changeinfo,name='user_changeinfo'),
    #下面是获取修改邮箱的验证码的路由
    re_path(r'^user_changeemail/$',views.user_changeemail,name='user_changeemail'),
    #下面是用户完成修改邮箱的路由
    re_path(r'^user_resetemail/$',views.user_resetemail,name='user_resetemail'),
    #下面是用户中心我的课程的路由
    re_path(r'^user_course/$',views.user_course,name='user_course'),
    #下面是用户中心我的收藏的默认页面的路由
    re_path(r'^user_loveorg/$',views.user_loveorg,name='user_loveorg'),
    #下面是用户中心我的收藏之收藏老师页面的路由
    re_path(r'^user_loveteacher/$',views.user_loveteacher,name='user_loveteacher'),
    #下面是用户中心我的收藏之收藏课程页面的路由
    re_path(r'^user_lovecourse/$',views.user_lovecourse,name='user_lovecourse'),
    #下面是用户中心我的消息页面的路由
    re_path(r'^user_message/$',views.user_message,name='user_message'),
]