from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.

class CityInfo(models.Model):
    '''城市信息模型'''
    name=models.CharField(max_length=20,verbose_name='城市名称')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回的描述信息'''
        return self.name

    class Meta:
        '''元信息'''
        verbose_name='城市信息'
        verbose_name_plural=verbose_name

class OrgInfo(models.Model):
    '''机构信息模型'''
    image=models.ImageField(upload_to='org/',max_length=200,verbose_name='机构图片')
    name=models.CharField(max_length=20,verbose_name='机构名称')
    course_num=models.IntegerField(default=0,verbose_name='课程数')
    study_num=models.IntegerField(default=0,verbose_name='学习人数')
    address=models.CharField(max_length=200,verbose_name='机构地址')
    desc=models.CharField(max_length=200,verbose_name='机构简介')
    detail=UEditorField(verbose_name='机构详情',width=700,height=400,toolbars='full',
    imagePath='ueditor/images/',filePath='ueditor/files/',upload_settings={'imageMaxSizing':1024000},
    default='')

    love_num=models.IntegerField(default=0,verbose_name='收藏数')
    click_num=models.IntegerField(default=0,verbose_name='访问量')
    category=models.CharField(choices=(('training','培训机构'),('university','高校'),('personal','个人')),max_length=20,verbose_name='机构类别')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    cityinfo=models.ForeignKey(CityInfo,verbose_name='所在城市',on_delete=models.CASCADE)

    def __str__(self):
        '''返回的描述'''
        return self.name

    class Meta:
        '''元信息'''
        verbose_name='机构信息'
        verbose_name_plural=verbose_name

class TeacherInfo(models.Model):
    '''老师信息的模型表'''
    image=models.ImageField(upload_to='teacher/',max_length=200,verbose_name='讲师头像')
    name=models.CharField(max_length=20,verbose_name='讲师姓名')
    work_year=models.IntegerField(default=3,verbose_name='工作年限')
    work_position=models.CharField(max_length=20,verbose_name='工作职位')
    work_style=models.CharField(max_length=20,verbose_name='教学特点')
    work_company=models.ForeignKey(OrgInfo,verbose_name='所属机构',on_delete=models.CASCADE)
    age=models.IntegerField(default=30,verbose_name='讲师年龄')
    gender=models.CharField(choices=(('girl','女'),('boy','男')),default='boy',verbose_name='讲师性别',max_length=10)
    love_num=models.IntegerField(default=0,verbose_name='收藏数')
    click_num=models.IntegerField(default=0,verbose_name='点击量')
    add_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        '''返回描述信息'''
        return self.name

    class Meta:
        '''元信息'''
        verbose_name='讲师信息'
        verbose_name_plural=verbose_name



