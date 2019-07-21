from . import views
from django.urls import re_path

urlpatterns=[
    #这是课程列表页的路由
    re_path(r'^course_list/$',views.course_list,name='course_list'),
    #这是课程详情页的路由
    re_path(r'^course_detail/(\d+)/$',views.course_detail,name="course_detail"),
    #下面是视频页面的路由
    re_path(r'^course_video/(\d+)/$',views.course_video,name='course_video'),
    #下面是课程评论页面的路由
    re_path(r'^course_comment/(\d+)/$',views.course_comment,name='course_comment'),
]