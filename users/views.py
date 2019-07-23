from django.shortcuts import render,redirect,reverse,HttpResponse
from . forms import UserRegisterForm,UserLoginForm,UserForgetForm,UserResetForm,UserChangeimageForm,UserChangeinfoForm,UserChangeemailForm,UserResetemailForm
from . models import UserProfile,EmailVerifyCode,BannerInfo
from operations.models import UserCourse,UserLove,UserMessage
from orgs.models import OrgInfo,TeacherInfo
from courses.models import CourseInfo
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from utils.send_mail_tool import send_email_code
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def index(request):
    '''这是主页的视图'''
    all_banners=BannerInfo.objects.all().order_by('-add_time')[:5]
    banner_courses=CourseInfo.objects.filter(is_banner=True)[:3]
    all_courses=CourseInfo.objects.filter(is_banner=False)[:6]
    all_orgs=OrgInfo.objects.all()[:15]
    return render(request,'index.html',{'all_banners':all_banners,'banner_courses':banner_courses,'all_courses':all_courses,'all_orgs':all_orgs})


def user_register(request):
    '''这是用户注册的视图'''
    if request.method=='GET':
        #这里把表单类的实例返回去是为了用验证码
        user_register_from=UserRegisterForm()
        return render(request,'users/register.html',{'user_register_form':user_register_from})
    else:
        user_register_form=UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email=user_register_form.cleaned_data['email']
            password=user_register_form.cleaned_data['password']
            #Q对象用于处理或关系的查询
            user_list=UserProfile.objects.filter(Q(username=email)|Q(email=email))

            if user_list:
                return render(request,'register.html',{'msg':'用户已经存在'})
            else:
                new_user=UserProfile()
                new_user.username=email
                new_user.set_password(password)
                new_user.email=email
                new_user.save()
                #向用户的邮箱发送验证码，用于激活用户
                send_email_code(email,1)
                return HttpResponse('请尽快前往您的邮箱激活,否则无法登录')
                #return redirect(reverse('index'))
        #下面是验证不通过的情况
        else:
            return render(request,'register.html',{'user_register_form':user_register_form})

def user_login(request):
    '''这是用户登录的视图'''
    if request.method=='GET':
        return render(request,'users/login.html')
    else:
        user_login_form=UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email=user_login_form.cleaned_data['email']
            password=user_login_form.cleaned_data['password']
            
            #这个方法验证的就是username和password，不要换成别的字段
            user=authenticate(username=email,password=password)
            #邮箱和密码验证通过
            if user:
                #已经被激活的用户可以登录
                if user.is_start:
                    login(request,user)
                    #用户每次登录成功，就给他发一个系统消息，欢迎他登录
                    msg=UserMessage()
                    msg.message_man=user.id
                    msg.message_content='欢迎登录。'
                    msg.save()
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请去您的邮箱激活您的账号,否则无法登录')
            #验证未通过
            else:
                return render(request,'users/login.html',{'msg':'邮箱或者密码有误'})
        #如果邮箱密码填写格式不对
        else:
            return render(request,'users/login.html',{'user_login_form':user_login_form})

def user_logout(request):
    '''这是用户退出的视图'''
    logout(request)
    return redirect(reverse('index'))

def user_active(request,code):
    '''这是处理用户激活的视图'''
    if code:
        evc_list=EmailVerifyCode.objects.filter(code=code)
        #如果在邮箱验证码表里有这样的验证码，就拿到邮箱，再通过邮箱找到用户
        if evc_list:
            evc=evc_list[0]
            email=evc.email
            user_list=UserProfile.objects.filter(username=email)
            if user_list:
                user=user_list[0]
                user.is_start=True
                user.save()
                return redirect(reverse('users:user_login'))
            else:
                pass
        else:
            pass
    else:
        pass


def user_forget(request):
    '''这是用户忘记密码的视图'''
    if request.method=='GET':
        #把这个空表单传过去是为了传验证码
        user_forget_form=UserForgetForm()
        return render(request,'forgetpwd.html',{'user_forget_form':user_forget_form})
    else:
        user_forget_form=UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email=user_forget_form.cleaned_data['email']
            user_list=UserProfile.objects.filter(username=email)
            #如果用户的邮箱存在
            if user_list:
                send_email_code(email,2)
                return HttpResponse('请尽快去您的邮箱重置密码')
            else:
                return render(request,'users/forgetpwd.html',{'msg':'用户不存在'})
        else:
            return render(request,'users/forgetpwd.html',{'user_forget_form':user_forget_form})

def user_reset(request,code):
    '''这是修改密码的视图'''
    if code:
        if request.method=='GET':
            return render(request,'users/password_reset.html',{'code':code})
        else:
            user_reset_form=UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password=user_reset_form.cleaned_data['password']
                password1=user_reset_form.cleaned_data['password1']
                if password==password1:
                    evc_list=EmailVerifyCode.objects.filter(code=code)
                    if evc_list:
                        evc=evc_list[0]
                        email=evc.email
                        user_list=UserProfile.objects.filter(username=email)
                        if user_list:
                            user=user_list[0]
                            user.set_password(password)
                            user.save()
                            return redirect(reverse('users:user_login'))
                        #如果用户不存在
                        else:
                            pass
                    #如果验证码不正确
                    else:
                        pass
                #如果输入的两个密码不一致
                else:
                    return render(request,'users/password_reset.html',{'msg':'两次密码不一致','code':code})
            #如果用户输入的格式错误
            else:
                return render(request,'users/password_reset.html',{'user_reset_form':user_reset_form})

def user_info(request):
    '''这是用户个人中心首页的视图'''
    return render(request,'users/usercenter-info.html')     

def user_changeimage(request):
    '''这是用户修改头像的视图'''
    #因为传过来的是图片，所以这里还要写第二个参数request.FILES
    #因为已经传入了一个已经存在的实例，所以不会创建新用户，而是修改老用户的头像
    user_changeimage_form=UserChangeimageForm(request.POST,request.FILES,instance=request.user)
    if user_changeimage_form.is_valid():
        user_changeimage_form.save(commit=True)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'fail'})

def user_changeinfo(request):
    '''这是用户普通信息修改的视图'''
    user_changeinfo_form=UserChangeinfoForm(request.POST,instance=request.user)
    if user_changeinfo_form.is_valid():
        user_changeinfo_form.save(commit=True)
        return JsonResponse({'status':'ok','msg':'修改成功'})
    else:
        return JsonResponse({'status':'fail','msg':'修改失败'})

def user_changeemail(request):
    '''
    这是用户修改邮箱的视图。当用户修改邮箱点击获取验证码的时候，会通过这个视图处理，发送邮箱验证码。
    :param request:http请求对象
    :return 返回json数据，在模板页面中处理
    '''
    user_changeemail_form=UserChangeemailForm(request.POST)
    if user_changeemail_form.is_valid():
        email=user_changeemail_form.cleaned_data['email']
        #看看这个邮箱是否已经被占用
        user_list=UserProfile.objects.filter(Q(email=email)|Q(username=email))
        if user_list:
            return JsonResponse({'status':'fail','msg':'邮箱已经被绑定'})
        else:
            #查看验证码表中是否已经给这个邮箱发送过send_type为3的邮件
            email_ver_list=EmailVerifyCode.objects.filter(email=email,send_type=3)
            if email_ver_list:
                #如果发送过，找到最近发送的那一条记录
                email_ver=email_ver_list.order_by('-add_time')[0]
                #判断当前时间和最近发送的验证码添加时间之差
                if (datetime.now()-email_ver.add_time).seconds > 60:
                    send_email_code(email,3)
                    #因为已经发了新的，所以旧的就可以删除了
                    email_ver.delete()
                    return JsonResponse({'status':'ok','msg':'请尽快去邮箱中获取验证码'})
                else:
                    return JsonResponse({'status':'fail','msg':'请不要重复发送验证码，1分钟后重试'})
            #如果从来没有发送过这种验证码，就直接发送
            else:
                send_email_code(email,3)
                return JsonResponse({'status':'ok','msg':'请尽快去邮箱中获取验证码'})
    else:
        return JsonResponse({'status':'fail','msg':'您的邮箱有误，请查证。'})

def user_resetemail(request):
    '''
    这是用户完成修改邮箱的视图。
    param:request http请求
    return json数据
    '''
    user_resetemail_form=UserResetemailForm(request.POST)
    if user_resetemail_form.is_valid():
        email=user_resetemail_form.cleaned_data['email']
        code=user_resetemail_form.cleaned_data['code']
        email_ver_list=EmailVerifyCode.objects.filter(email=email,code=code)
        if email_ver_list:
            email_ver=email_ver_list[0]
            #判断这个验证码是否还在有效期
            if (datetime.now()-email_ver.add_time).seconds < 300:
                request.user.username=email
                request.user.email=email
                request.user.save()
                return JsonResponse({'status':'ok','msg':'邮箱修改成功'})
            else:
                return JsonResponse({'status':'fail','msg':'验证码失效，请重新发送验证码'})
        else:
            return JsonResponse({'status':'fail','msg':'您的邮箱或者验证码有误'})
    else:
        return JsonResponse({'status':'fail','msg':'您的邮箱或者验证码不合法'})


def user_course(request):
    '''这是用户中心我的课程的视图'''
    usercourse_list=request.user.usercourse_set.all()
    course_list=[ usercourse.study_course for usercourse in usercourse_list]
    return render(request,'users/usercenter-mycourse.html',{'course_list':course_list})
    
def user_loveorg(request):
    '''这是用户中心的用户收藏的默认视图'''
    userloveorg_list=UserLove.objects.filter(love_man=request.user,love_type=1,love_status=True)
    orgid_list=[userloveorg.love_id for userloveorg in userloveorg_list]
    org_list=OrgInfo.objects.filter(id__in=orgid_list)
    return render(request,'users/usercenter-fav-org.html',{'org_list':org_list})

def user_loveteacher(request):
    '''下面是用户中心的用户收藏之收藏老师的视图'''
    userloveteacher_list=UserLove.objects.filter(love_man=request.user,love_type=3,love_status=True)
    teacherid_list=[userloveteacher.love_id for userloveteacher in userloveteacher_list]
    teacher_list=TeacherInfo.objects.filter(id__in=teacherid_list)
    return render(request,'users/usercenter-fav-teacher.html',{'teacher_list':teacher_list})

def user_lovecourse(request):
    '''这是用户中心的用户收藏之收藏课程的视图'''
    userlovecourse_list=UserLove.objects.filter(love_man=request.user,love_type=2,love_status=True)
    courseid_list=[ userlovecourse.love_id for userlovecourse in userlovecourse_list]
    course_list=CourseInfo.objects.filter(id__in=courseid_list)
    return render(request,'users/usercenter-fav-course.html',{'course_list':course_list})

def  user_message(request):
    '''这是用户中心的用户消息视图'''
    msg_list=UserMessage.objects.filter(message_man=request.user.id)
    return render(request,'users/usercenter-message.html',{'msg_list':msg_list})
