from django.shortcuts import render
from . models import CourseInfo
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

def course_list(request):
    '''这是公开课页面的视图'''
    all_courses=CourseInfo.objects.all()
    recommend_courses=all_courses.order_by('-add_time')[:3]

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
    })

def course_detail(request,course_id):
    '''这是课程详情页面的视图'''
    if course_id:
        print(course_id)
        course=CourseInfo.objects.filter(id=int(course_id))[0]

        #下面是相关的课程(要排除该课程本身)
        related_courses=CourseInfo.objects.filter(category=course.category).exclude(id=course.id)[:2]
        return render(request,'courses/course-detail.html',{'course':course,'related_courses':related_courses})