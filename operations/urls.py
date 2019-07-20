from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^user_ask/$',views.user_ask,name='user_ask'),
    #下面是用户收藏的路由
    re_path(r'^user_love/$',views.user_love,name='user_love'),
]