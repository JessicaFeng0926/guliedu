from django.db import models
from users.models import UserProfile
from courses.models import CourseInfo

# Create your models here.

class UserAsk(models.Model):
    '''用户咨询模型'''
    name=models.CharField(max_length=30,verbose_name='姓名')
    phone=models.CharField(max_length=11,verbose_name='手机')
    course=models.CharField(max_length=20,verbose_name='课程')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='咨询时间')

    def __str__(self):
        '''返回的描述'''
        return self.name

    class Meta:
        '''元信息类'''
        verbose_name='咨询信息'
        verbose_name_plural=verbose_name

class UserLove(models.Model):
    '''这是收藏的模型类'''
    love_man=models.ForeignKey(UserProfile,verbose_name='收藏用户',on_delete=models.CASCADE)
    love_id=models.IntegerField(verbose_name='收藏ID')
    love_type=models.IntegerField(choices=((1,'org'),(2,'course'),(3,'teacher')),verbose_name='收藏类型')
    love_status=models.BooleanField(default=False,verbose_name='收藏状态')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='收藏时间')

    def __str__(self):
        '''这是返回的描述'''
        return self.love_man.username

    class Meta:
        '''元信息类'''
        verbose_name='收藏信息'
        verbose_name_plural=verbose_name

class UserCourse(models.Model):
    '''用户学习模型'''
    study_man=models.ForeignKey(UserProfile,verbose_name='学习用户',on_delete=models.CASCADE)
    study_course=models.ForeignKey(CourseInfo,verbose_name='学习课程',on_delete=models.CASCADE)
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='学习时间')

    def __str__(self):
        '''这是返回的描述'''
        return self.study_man.username

    class Meta:
        '''元信息类'''
        #联合唯一，以后这个用户再学习这个课程不会重复添加
        unique_together=('study_man','study_course')
        verbose_name='用户课程信息'
        verbose_name_plural=verbose_name

class UserComment(models.Model):
    '''这是用户评论的模型类'''
    comment_man=models.ForeignKey(UserProfile,verbose_name='评论的用户',on_delete=models.CASCADE)
    comment_course=models.ForeignKey(CourseInfo,verbose_name='评论的课程',on_delete=models.CASCADE)
    comment_content=models.CharField(max_length=300,verbose_name='评论内容')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    def __str__(self):
        '''这是返回的描述'''
        return self.comment_content

    class Meta:
        '''元信息类'''
        verbose_name='用户评论信息'
        verbose_name_plural=verbose_name

class UserMessage(models.Model):
    '''这是用户消息模型类'''
    #如果这里的id是0就是给所有用户发消息，如果是一个用户id，就是给单独的人发消息
    #这样可以区分群消息和个人消息
    message_man=models.IntegerField(default=0,verbose_name='消息接受者id')
    message_content=models.CharField(max_length=200,verbose_name='消息内容')
    message_status=models.BooleanField(default=False,verbose_name='消息状态')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='发送消息时间')

    def __str__(self):
        '''这是返回的描述'''
        return self.message_content

    class Meta:
        '''元信息类'''
        verbose_name='用户消息信息'
        verbose_name_plural=verbose_name


    





