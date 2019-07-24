"""guliedu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from users.views import handler_404,handler_500
import xadmin
#from users.views import index
from users.views import IndexView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),
    re_path(r'^users/',include(('users.urls','users'),namespace='users')),
    re_path(r'^courses/',include(('courses.urls','courses'),namespace='courses')),
    re_path(r'^orgs/',include(('orgs.urls','orgs'),namespace='orgs')),
    re_path(r'^operations/',include(('operations.urls','operations'),namespace='operations')),
    #re_path(r'^$',index,name='index'),
    #给验证码app captcha也分发路由,它不需要app名字也不需要namespace,加了多余的东西会报错
    re_path(r'^captcha/',include('captcha.urls')),
    #我们已经把主页的view变成了类，所以这里的写法有些不同
    re_path(r'^$',IndexView.as_view(),name='index'),
    #给富文本编辑器ueditor配置路由
    re_path(r'^ueditor/',include('DjangoUeditor.urls')),


]

#配置404页面的视图
handler404=handler_404
handler500=handler_500