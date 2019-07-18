from django.shortcuts import render
from . models import OrgInfo,CityInfo,TeacherInfo

# Create your views here.

def org_list(request):
    '''这是机构列表视图'''
    all_orgs=OrgInfo.objects.all()
    return render(request,'org-list.html',{'all_orgs':all_orgs})
