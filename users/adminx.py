'''这是我们的站点配置文档，注意千万不能叫xadmin.py，因为会跟已经存在的文件重命'''
import xadmin
from . models import BannerInfo,EmailVerifyCode
from xadmin import views

class BaseXadminSetting(object):
    '''这是管理站点主题配置类'''
    enable_themes=True
    use_bootswatch=True
    

class CommXadminSetting(object):
    '''这是设置全局外观的类'''
    #更改了站点的名字
    site_title='谷粒教育后台管理系统'
    #更改了页脚的名字
    site_footer='尚硅谷IT教育'
    #让左侧的菜单能够收缩
    menu_style='accordion'


#用户的模型类不要在这里注册，会跟xadmin自动生成的用户信息冲突

class BannerInfoXadmin(object):
    '''这是轮播图的管理类'''
    list_display=['image','url','add_time']
    search_fields=['image','url']
    list_filter=['image','url']
    #下面这个是使用了font awesome里的图标，就像glyphicon一样，使站点的模型名字前面有一个可爱的图标
    model_icon='fa fa-file-image-o'

class EmailVerifyCodeXadmin(object):
    '''邮箱验证表的管理类'''
    list_display=['code','email','send_type','add_time']
    model_icon='fa fa-envelope'
    
    
#注册模型管理类
xadmin.site.register(BannerInfo,BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode,EmailVerifyCodeXadmin)

#注册xadmin主题配置类，注册以后我们就有很多可以选的很漂亮的主题啦
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
#注册全局样式类
xadmin.site.register(views.CommAdminView,CommXadminSetting)
