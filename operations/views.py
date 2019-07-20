from django.shortcuts import render
from . forms import UserAskForm
from django.http import JsonResponse
from . models import UserLove

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


def user_love(request):
    '''这是处理用户收藏的视图'''
    love_id=request.GET.get('love_id','')
    love_type=request.GET.get('love_type','')
    if love_id and love_type:
        #如果收藏的id和type同时存在，要去收藏表中查找有没有当前用户的收藏记录
        love = UserLove.objects.filter(love_id=int(love_id),love_type=int(love_type),love_man=request.user)
        if love:
            #如果有这条收藏记录，需要判断收藏状态是True还是False，True代表收藏过，并且现在的页面上应该显示的是取消收藏
            #这次点击是为了取消收藏
            if love[0].love_status:
                love[0].love_status=False
                love[0].save()
                return JsonResponse({'status':'ok','msg':'收藏'})
            #如果收藏状态是False，代表他以前收藏过并且已经取消了收藏，这次点击是为了重新收藏，页面上现在显示的是收藏
            else:
                love[0].love_status=True
                love[0].save()
                return JsonResponse({'status':'ok','msg':'取消收藏'})
        #如果找不到love对象，代表该用户从未收藏过，所以需要先创建一个对象,并且把收藏状态设为True
        else:
            new_love=UserLove()
            new_love.love_man=request.user
            new_love.love_id=int(love_id)
            new_love.love_type=int(love_type)
            new_love.love_status=True
            new_love.save()
            return JsonResponse({'status':'ok','msg':'取消收藏'})
    #如果loveid和lovetype不同时存在
    else:
        return JsonResponse({'status':'fail','msg':'收藏失败'})

            







        



