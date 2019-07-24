from django.shortcuts import render
from . models import CourseInfo
from orgs.models import OrgInfo
from operations.models import UserLove,UserCourse,UserComment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from utils.decorator import login_decorator
# Create your views here.

def course_list(request):
    '''这是公开课页面的视图'''
    all_courses=CourseInfo.objects.all()
    recommend_courses=all_courses.order_by('-add_time')[:3]

    #下面是全局搜索过滤
    keyword=request.GET.get('keyword','')
    if keyword:
        all_courses=all_courses.filter(Q(name__icontains=keyword)|Q(desc__icontains=keyword)|Q(detail__icontains=keyword))

    sort=request.GET.get('sort','')
    if sort:
        all_courses=all_courses.order_by('-'+sort)

    #实例化分页器
    pa=Paginator(all_courses,3)
    pagenum=request.GET.get('pagenum')
    try:
        current_page=pa.get_page(pagenum)
        print(type(pagenum))
    except PageNotAnInteger:
        current_page=pa.get_page(1)
    except EmptyPage:
        current_page=pa.get_page(pa.num_pages)


    return render(request,'courses/course-list.html',
    {'current_page':current_page,
    'recommend_courses':recommend_courses,
    'sort':sort,
    'all_courses':all_courses,
    'keyword':keyword,
    })

def course_detail(request,course_id):
    '''这是课程详情页面的视图'''
    if course_id:
        course=CourseInfo.objects.filter(id=int(course_id))[0]

        #只要点进了课程的详情页，就把该课程的点击量加一
        course.click_num+=1
        course.save()
        #下面是看看课程和机构有没有收藏
        love_course_status=False
        love_org_status=False
        if request.user.is_authenticated:
            user_course_love=UserLove.objects.filter(love_man=request.user,love_id=course.id,love_type=2,love_status=True)
            user_org_love=UserLove.objects.filter(love_man=request.user,love_id=course.orginfo.id,love_type=1,love_status=True)
            if user_course_love:
                love_course_status=True
            if user_org_love:
                love_org_status=True

        #下面是相关的课程(要排除该课程本身)
        related_courses=CourseInfo.objects.filter(category=course.category).exclude(id=course.id)[:2]
        return render(request,'courses/course-detail.html',{'course':course,'related_courses':related_courses,
        'love_course_status':love_course_status,'love_org_status':love_org_status})

#@login_required(login_url='/users/user_login/')
#django提供的装饰器不能满足我们的需求，我们要自己写装饰器

@login_decorator
def course_video(request,course_id):
    if course_id:
        course=CourseInfo.objects.filter(id=int(course_id))[0]

        #只要用户点击了开始学习按钮，就要把它添加到UserCourse表里，但要先检查一下是否已经添加过了
        usercourse_list=UserCourse.objects.filter(study_man=request.user,study_course=course)
        if not usercourse_list:
            
            #给课程的学习人数增加1
            course.study_num+=1
            course.save()
            #给课程所属的机构的学习人数加一(前提是这个用户没学过这个机构的任何课程)
            #第一步，查找当前用户学习的所有课程
            usercourse_list=UserCourse.objects.filter(study_man=request.user)
            print(usercourse_list)
            course_list=[usercourse.study_course for usercourse in usercourse_list]
            print(course_list)
            #第二步，判断这些课程是否都不是这个机构的
            org_list=list(set([ c.orginfo for c in course_list]))
            print(org_list)
            if course.orginfo not in org_list:
                course.orginfo.study_num+=1
                course.orginfo.save()
            
            #必须最后存入UserCourse表，否则跟前面的机构的逻辑矛盾（新增的课程就是这个机构，那么就不需要再给机构加学习人数了）
            usercourse=UserCourse()
            usercourse.study_man=request.user
            usercourse.study_course=course
            usercourse.save()

        #下面是找出学过这门课的同学还学过什么课
        #第一步，找到UserCourse里所有跟这门课有关的对象
        usercourse_list=UserCourse.objects.filter(study_course=course)
        #第二步，遍历找出所有学过这门课的学生
        user_list=[usercourse.study_man for usercourse in usercourse_list]
        #第三步，找出这些用户还学过什么课程,拿出所有的UserCourse对象,要除去这门课本身(这里用了filter里的in)
        usercourse_list=UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
        #第四步，拿出所有的课程对象
        course_list=list(set([usercourse.study_course for usercourse in usercourse_list ]))

        return render(request,'courses/course-video.html',{'course':course,'course_list':course_list})

def course_comment(request,course_id):
    '''下面是课程评论页面的视图'''
    if course_id:
        course=CourseInfo.objects.filter(id=int(course_id))[0]
        all_comments=course.usercomment_set.all()[:10]

        #下面寻找学过该课程的同学还学过什么
        usercourse_list=UserCourse.objects.filter(study_course=course)
        user_list=[ usercourse.study_man for usercourse in usercourse_list]
        usercourse_list=UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
        course_list=list(set([ usercourse.study_course for usercourse in usercourse_list]))

        return render(request,'courses/course-comment.html',{'course':course,'all_comments':all_comments,'course_list':course_list})
