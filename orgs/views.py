from django.shortcuts import render
from . models import OrgInfo,CityInfo,TeacherInfo
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
        print(type(category))
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
    return render(request,'org-list.html',{'all_orgs':all_orgs,'all_cities':all_cities,'sort_orgs':sort_orgs,'current_page':current_page,'category':category,'cityid':cityid,'sort':sort})
