from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^org_list/$',views.org_list,name='org_list'),
    
]