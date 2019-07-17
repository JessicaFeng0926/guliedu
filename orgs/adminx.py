import xadmin
from . models import CityInfo,OrgInfo,TeacherInfo

class CityInfoXadmin(object):
    '''城市信息管理类'''
    list_display=['name','add_time']
    model_icon='fa fa-building'
    

class OrgInfoXadmin(object):
    '''机构信息管理类'''
    list_display=['image','name','course_num','study_num','love_num','click_num','category','cityinfo']
    model_icon='fa fa-institution'

class TeacherInfoXadmin(object):
    '''老师信息的管理类'''
    list_display=['image','name','work_year','work_position','work_company','age','gender','love_num']
    model_icon='fa fa-mortar-board'
    
#注册
xadmin.site.register(CityInfo,CityInfoXadmin)
xadmin.site.register(OrgInfo,OrgInfoXadmin)
xadmin.site.register(TeacherInfo,TeacherInfoXadmin)