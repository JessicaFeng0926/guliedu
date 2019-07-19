from django.shortcuts import render
from . forms import UserAskForm
from django.http import JsonResponse

# Create your views here.

def user_ask(request):
    '''这是处理用户咨询的视图'''
    user_ask_form=UserAskForm(request.POST)
    if user_ask_form.is_valid():
        #这个表单类对象保存了，model就保存了，不需要单独操作model
        user_ask_form.save(commit=True)
        return JsonResponse({'status':'ok','msg':'咨询成功'})
    else:
        return JsonResponse({'status':'fail','msg':'咨询失败'})


        



