from django.db import models
from orgs.models import OrgInfo,TeacherInfo

# Create your models here.

class CourseInfo(models.Model):
    '''课程信息模型类'''
    image=models.ImageField(upload_to='course/',max_length=200,verbose_name='课程封面')
    name=models.CharField(max_length=20,verbose_name='课程名称')
    study_time=models.IntegerField(default=0,verbose_name='学习时长')
    study_num=models.IntegerField(default=0,verbose_name='学习人数')
    level=models.CharField(choices=(('advanced','高级'),('intermediate','中级'),('beginning','初级')),max_length=20,default='beginning',verbose_name='课程难度')
    love_num=models.IntegerField(default=0,verbose_name='收藏数')
    click_num=models.IntegerField(default=0,verbose_name='点击量')
    desc=models.CharField(max_length=200,verbose_name='课程简介')
    detail=models.TextField(verbose_name='课程详情')
    category=models.CharField(choices=(('front_end','前端开发'),('back_end','后端开发')),verbose_name='课程类别',max_length=15)
    course_notice=models.CharField(max_length=200,verbose_name='课程公告')
    course_need=models.CharField(max_length=200,verbose_name='课程须知')
    teacher_tell=models.CharField(max_length=100,verbose_name='老师教导')
    orginfo=models.ForeignKey(OrgInfo,verbose_name='所属机构',on_delete=models.CASCADE)
    teacherinfo=models.ForeignKey(TeacherInfo,verbose_name='所属讲师',on_delete=models.CASCADE)
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回的描述'''
        return self.name

    class Meta:
        '''元信息'''
        verbose_name='课程信息'
        verbose_name_plural=verbose_name


class LessonInfo(models.Model):
    '''这是章节信息模型类'''
    name=models.CharField(max_length=50,verbose_name='章节名称')
    courseinfo=models.ForeignKey(CourseInfo,verbose_name='所属课程',on_delete=models.CASCADE)
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回的描述'''
        return self.name

    class Meta:
        '''元信息类'''
        verbose_name='章节信息'
        verbose_name_plural=verbose_name

class VideoInfo(models.Model):
    '''这是视频的模型类'''
    name=models.CharField(max_length=50,verbose_name='视频名称')
    study_time=models.IntegerField(default=0,verbose_name='视频时长')
    url=models.URLField(default='http://www.atguitu.com',verbose_name='视频链接',max_length=200)
    lessoninfo=models.ForeignKey(LessonInfo,verbose_name='所属章节',on_delete=models.CASCADE)
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回描述'''
        return self.name

    class Meta:
        '''元信息类'''
        verbose_name='视频信息'
        verbose_name_plural=verbose_name

class SourceInfo(models.Model):
    '''资源模型类'''
    name=models.CharField(max_length=50,verbose_name='资源名称')
    download=models.FileField(upload_to='source/',verbose_name='下载路径',max_length=200)
    courseinfo=models.ForeignKey(CourseInfo,verbose_name='所属课程',on_delete=models.CASCADE)
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回的描述'''
        return self.name

    class Meta:
        '''元信息类'''
        verbose_name='资源信息'
        verbose_name_plural=verbose_name

        
    


