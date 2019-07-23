from django.shortcuts import render
from . forms import UserAskForm,UserCommentForm
from django.http import JsonResponse
from . models import UserLove,UserComment,UserMessage
from courses.models import CourseInfo
from orgs.models import OrgInfo,TeacherInfo

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
        if int(love_type)==1:
            obj=OrgInfo.objects.filter(id=int(love_id))[0]
        elif int(love_type)==2:
            obj=CourseInfo.objects.filter(id=int(love_id))[0]
        elif int(love_type)==3:
            obj=TeacherInfo.objects.filter(id=int(love_id))[0]
        #如果收藏的id和type同时存在，要去收藏表中查找有没有当前用户的收藏记录
        love = UserLove.objects.filter(love_id=int(love_id),love_type=int(love_type),love_man=request.user)
        if love:
            #如果有这条收藏记录，需要判断收藏状态是True还是False，True代表收藏过，并且现在的页面上应该显示的是取消收藏
            #这次点击是为了取消收藏
            if love[0].love_status:
                love[0].love_status=False
                love[0].save()
                
                obj.love_num-=1
                obj.save()
                return JsonResponse({'status':'ok','msg':'收藏'})
            #如果收藏状态是False，代表他以前收藏过并且已经取消了收藏，这次点击是为了重新收藏，页面上现在显示的是收藏
            else:
                love[0].love_status=True
                love[0].save()

                obj.love_num+=1
                obj.save()
                return JsonResponse({'status':'ok','msg':'取消收藏'})
        #如果找不到love对象，代表该用户从未收藏过，所以需要先创建一个对象,并且把收藏状态设为True
        else:
            new_love=UserLove()
            new_love.love_man=request.user
            new_love.love_id=int(love_id)
            new_love.love_type=int(love_type)
            new_love.love_status=True
            new_love.save()
            
            obj.love_num+=1
            obj.save()
            return JsonResponse({'status':'ok','msg':'取消收藏'})
    #如果loveid和lovetype不同时存在
    else:
        return JsonResponse({'status':'fail','msg':'收藏失败'})

def user_comment(request):
    '''这是处理用户评论的视图'''
    comment_course_id=request.POST.get('comment_course_id')
    user_comment_form=UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        user_comment_form.save(commit=False)
        user_comment_form.instance.comment_man_id=request.user.id
        user_comment_form.instance.comment_course_id=comment_course_id
        user_comment_form.save(commit=True)
        return JsonResponse({'status':'ok','msg':'评论成功'})
    else:
        return JsonResponse({'status':'fail','msg':'评论失败'})

def user_deletelove(request):
    '''这是用户在个人中心删除收藏的视图'''
    love_id=request.GET.get('love_id','')
    love_type=request.GET.get('love_type','')
    if love_id and love_type:
        love=UserLove.objects.filter(love_id=int(love_id),love_type=int(love_type),love_status=True)
        if love:
            love[0].love_status=False
            love[0].save()
            return JsonResponse({'status':'ok','msg':'取消成功'})
        else:
            return JsonResponse({'status':'fail','msg':'取消失败'})
    else:
        return JsonResponse({'status':'fail','msg':'取消失败'})

def user_deletemessage(request):
    '''这是用户在个人中心阅读消息的视图'''
    msg_id=request.GET.get('msg_id','')
    if msg_id:
        msg_list=UserMessage.objects.filter(id=int(msg_id))
        if msg_list:
            msg=msg_list[0]
            msg.message_status=True
            msg.save()
            return JsonResponse({'status':'ok','msg':'已读'})
        else:
            return JsonResponse({'status':'fail','msg':'读取失败'})
    else:
        return JsonResponse({'status':'fail','msg':'读取失败'})

        



