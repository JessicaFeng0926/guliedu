from django.shortcuts import render
from . models import OrgInfo,CityInfo,TeacherInfo
from operations.models import UserLove
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

def org_list(request):
    '''这是机构列表视图'''
    all_orgs=OrgInfo.objects.all()
    all_cities=CityInfo.objects.all()
    sort_orgs=all_orgs.order_by('-love_num')[:3]

    #按照机构类别进行过滤
    category=request.GET.get('category')
    #如果没有category这个参数，那么获取的是None
    #从第二次开始，这个参数就会变成字符串的None，因为是从模板那边接收过来的
    #还有一个简单的方法，就是category=request.GET.get('category',''),这样当取不到值的时候，默认值会一直是空字符串，不存在None和'None'的问题
    if category =='None' or category == None:
        pass
    else:
        all_orgs=all_orgs.filter(category=category)

    #按照所在城市进行过滤
    cityid=request.GET.get('cityid')
    if cityid == 'None' or cityid==None:
        pass
    else:
        all_orgs=all_orgs.filter(cityinfo_id=int(cityid))
    
    #按照学习人数排序
    sort=request.GET.get('sort','')
    if sort:
        all_orgs=all_orgs.order_by('-'+sort)

    #pagenum是get请求里的一个参数，在模板里能看到pagenum的定义
    pagenum=request.GET.get('pagenum')
    #实例化分页器
    pa=Paginator(all_orgs,3)
    try:
        current_page=pa.page(pagenum)
    #如果页码不是一个整数，那么可能是没有穿这个参数，这时就强制它获取第一页
    except PageNotAnInteger:
        current_page=pa.page(1)
    #如果发生了空页错误，那就是走到了末尾，这时强制它获取最后一页
    except EmptyPage:
        current_page=pa.page(pa.num_pages)


    #category也要传回去，跟分页的参数拼接到一起，不然会乱
    return render(request,'orgs/org-list.html',{'all_orgs':all_orgs,'all_cities':all_cities,'sort_orgs':sort_orgs,'current_page':current_page,'category':category,'cityid':cityid,'sort':sort})


def org_detail(request,org_id):
    '''这是机构详情主页的视图'''
    if org_id:
        org=OrgInfo.objects.filter(id=int(org_id))[0]
        #只要进了这个机构的详情页，这个机构的访问量就需要加一
        org.click_num+=1
        org.save()
        #在返回页面机构的时候也需要返回对本机构的收藏状态，这样才能根据实际情况显示收藏或者取消收藏，这里不能是死数据
        love_status=False
        if request.user.is_authenticated:
            love=UserLove.objects.filter(love_man=request.user,love_id=org.id,love_type=1,love_status=True)
            if love:
                love_status=True
        #传回一个detail_type数据是为了给css跟随提供判断依据
        return render(request,'orgs/org-detail-homepage.html',{'org':org,'detail_type':'home','love_status':love_status})

def org_detail_course(request,org_id):
    '''这是机构详情的课程页的视图'''
    if org_id:
        org=OrgInfo.objects.filter(id=int(org_id))[0]
        all_courses=org.courseinfo_set.all()
        #实例化分页器
        pa=Paginator(all_courses,4)
        pagenum=request.GET.get('pagenum')
        try:
            current_page=pa.get_page(pagenum)
        except PageNotAnInteger:
            current_page=pa.get_page(1)
        except EmptyPage:
            current_page=pa.get_page(pa.num_pages)
        #在返回页面机构的时候也需要返回对本机构的收藏状态，这样才能根据实际情况显示收藏或者取消收藏，这里不能是死数据
        love_status=False
        if request.user.is_authenticated:
            love=UserLove.objects.filter(love_man=request.user,love_id=org.id,love_type=1,love_status=True)
            if love:
                love_status=True

        return render(request,'orgs/org-detail-course.html',{'org':org,'current_page':current_page,'detail_type':'course','love_status':love_status})


def org_detail_desc(request,org_id):
    '''这是机构详情之机构介绍页面的视图'''
    if org_id:
        org=OrgInfo.objects.filter(id=int(org_id))[0]
        #在返回页面机构的时候也需要返回对本机构的收藏状态，这样才能根据实际情况显示收藏或者取消收藏，这里不能是死数据
        love_status=False
        if request.user.is_authenticated:
            love=UserLove.objects.filter(love_man=request.user,love_id=org.id,love_type=1,love_status=True)
            if love:
                love_status=True
        return render(request,'orgs/org-detail-desc.html',{'org':org,'detail_type':'desc','love_status':love_status})

def org_detail_teacher(request,org_id):
    '''这是机构详情之教师页面的视图'''
    if org_id:
        org=OrgInfo.objects.filter(id=int(org_id))[0]
        #在返回页面机构的时候也需要返回对本机构的收藏状态，这样才能根据实际情况显示收藏或者取消收藏，这里不能是死数据
        love_status=False
        if request.user.is_authenticated:
            love=UserLove.objects.filter(love_man=request.user,love_id=org.id,love_type=1,love_status=True)
            if love:
                love_status=True
        return render(request,'orgs/org-detail-teachers.html',{'org':org,'detail_type':'teacher','love_status':love_status})

def teacher_list(request):
    '''这是教师列表页的视图'''
    all_teachers=TeacherInfo.objects.all()

    #下面是根据人气排序
    sort=request.GET.get('sort','')
    if sort:
        all_teachers=all_teachers.order_by('-'+sort)

    #下面是分页器
    pa=Paginator(all_teachers,2)
    pagenum=request.GET.get('pagenum','')
    try:
        current_page=pa.get_page(pagenum)
    except PageNotAnInteger:
        current_page=pa.get_page(1)
    except EmptyPage:
        current_page=pa.get_page(pa.num_pages)
    #下面是讲师排行榜的数据，根据收藏数排行
    teacher_board=all_teachers.order_by('-love_num')[:2]
    return render(request,'orgs/teachers-list.html',{'all_teachers':all_teachers,'teacher_board':teacher_board,'current_page':current_page,'sort':sort})

def teacher_detail(request,teacher_id):
    '''这是教师详情页的视图'''
    if teacher_id:
        teacher=TeacherInfo.objects.filter(id=int(teacher_id))[0]

        #只要点进了老师的详情页，这个老师的点击量就加1
        teacher.click_num+=1
        teacher.save()

        #下面是获取教师排行榜的
        all_teachers=TeacherInfo.objects.all()
        teacher_board=all_teachers.order_by('-love_num')

        #下面是该教师收藏状态的数据
        teacher_love_status=False
        teacher_love=UserLove.objects.filter(love_id=teacher.id,love_type=3,love_man=request.user,love_status=True)
        if teacher_love:
            teacher_love_status=True
        #下面是该页面的机构收藏状态的数据
        org_love_status=False
        org_love=UserLove.objects.filter(love_id=teacher.work_company.id,love_type=1,love_man=request.user,love_status=True)
        if org_love:
            org_love_status=True
        return render(request,'orgs/teacher-detail.html',{'teacher':teacher,'teacher_board':teacher_board,'teacher_love_status':teacher_love_status,'org_love_status':org_love_status})