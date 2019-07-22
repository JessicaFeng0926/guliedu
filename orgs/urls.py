from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^org_list/$',views.org_list,name='org_list'),
    #下面是机构详情的主页的路由
    re_path(r'^org_detail/(\d+)/$',views.org_detail,name='org_detail'),
    #下面是机构详情的课程页的路由
    re_path(r'^org_detail_course/(\d+)/$',views.org_detail_course,name='org_detail_course'),
    #下面是机构详情的机构介绍页的路由
    re_path(r'^org_detail_desc/(\d+)/$',views.org_detail_desc,name='org_detail_desc'),
    #下面是机构详情的教师详情页的路由
    re_path(r'^org_detail_teacher/(\d+)/$',views.org_detail_teacher,name='org_detail_teacher'),
    #下面是授课教师的列表页路由
    re_path(r'^teacher_list/$',views.teacher_list,name='teacher_list'),
    #下面是授课教师详情页的路由
    re_path(r'^teacher_detail/(\d+)/$',views.teacher_detail,name='teacher_detail'),
]