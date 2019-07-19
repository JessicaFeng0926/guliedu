from . import views
from django.urls import re_path

urlpatterns=[
    re_path(r'^user_ask/$',views.user_ask,name='user_ask')
]