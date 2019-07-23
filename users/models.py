from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    '''这是用户信息表的模型类'''
    image=models.ImageField(upload_to='user/',max_length=200,verbose_name='用户头像',null=True,blank=True)
    nickname=models.CharField(max_length=20,verbose_name='用户昵称',null=True,blank=True)
    birthday=models.DateTimeField(verbose_name='用户生日',null=True,blank=True)
    gender=models.CharField(choices=(('girl','女'),('boy','男')),max_length=10,verbose_name='用户性别',default='girl')
    address=models.CharField(max_length=200,verbose_name='用户地址',null=True,blank=True)
    phone=models.CharField(max_length=11,verbose_name='用户手机',null=True,blank=True)
    #这是一个是否被激活的字段，没有被激活的用户不能登录
    is_start=models.BooleanField(default=False,verbose_name='是否激活')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''这是返回的描述'''
        return self.username

    def get_msg_counter(self):
        '''这是计算目前有多少未读消息的方法，用于显示在每个页面上面的喇叭处'''
        from operations.models import UserMessage
        counter=UserMessage.objects.filter(message_man=self.id,message_status=False).count()
        return counter


    class Meta:
        '''元信息类'''
        verbose_name='用户信息'
        verbose_name_plural=verbose_name


class BannerInfo(models.Model):
    '''这是轮播图的模型类'''
    image=models.ImageField(upload_to='banner/',verbose_name='轮播图片',max_length=200)
    url=models.URLField(default='http://www.atguigu.com',max_length=200,verbose_name='图片链接')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回的文字描述'''
        return str(self.image)

    class Meta:
        '''元信息'''
        verbose_name='轮播图信息'
        verbose_name_plural=verbose_name


class EmailVerifyCode(models.Model):
    '''邮箱验证表的模型类'''
    code=models.CharField(max_length=20,verbose_name='邮箱验证码')
    email=models.EmailField(max_length=200,verbose_name='验证码邮箱')
    send_type=models.IntegerField(choices=((1,'register'),(2,'forget'),(3,'change')),verbose_name='验证码类型')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回的文字性描述'''
        return self.code

    class Meta:
        '''元信息'''
        verbose_name='邮箱验证码信息'
        verbose_name_plural=verbose_name


