import xadmin
from . models import CourseInfo,LessonInfo,VideoInfo,SourceInfo

class CourseInfoXadmin(object):
    '''课程信息管理类'''
    list_display=['image','name','study_time','study_num','level','love_num']
    model_icon='fa fa-book'

class LessonInfoXadmin(object):
    '''这是章节信息管理类'''
    list_display=['name','courseinfo']
    model_icon='fa fa-bookmark'
    

class VideoInfoXadmin(object):
    '''这是视频的管理类'''
    list_display=['name','study_time','url']
    model_icon='fa fa-file-video-o'

class SourceInfoXadmin(object):
    '''资源管理类'''
    list_display=['name','download']
    model_icon='fa fa-file-zip-o'

#注册
xadmin.site.register(CourseInfo,CourseInfoXadmin)
xadmin.site.register(LessonInfo,LessonInfoXadmin)
xadmin.site.register(VideoInfo,VideoInfoXadmin)
xadmin.site.register(SourceInfo,SourceInfoXadmin)



        
    


