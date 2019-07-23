from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^user_ask/$',views.user_ask,name='user_ask'),
    #下面是用户收藏的路由
    re_path(r'^user_love/$',views.user_love,name='user_love'),
    #下面是用户评论的路由
    re_path(r'^user_comment/$',views.user_comment,name='user_comment'),
    #下面是在用户中心删除收藏的路由
    re_path(r'^user_deletelove/$',views.user_deletelove,name='user_deletelove'),
    #下面是在用户中心把未读消息变为已读的路由
    re_path(r'^user_deletemessage/$',views.user_deletemessage,name='user_deletemessage'),
]