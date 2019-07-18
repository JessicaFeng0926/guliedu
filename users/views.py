from django.shortcuts import render,redirect,reverse,HttpResponse
from . forms import UserRegisterForm,UserLoginForm,UserForgetForm,UserResetForm
from . models import UserProfile,EmailVerifyCode
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from utils.send_mail_tool import send_email_code

# Create your views here.
def index(request):
    '''这是主页的视图'''
    return render(request,'index.html')


def user_register(request):
    '''这是用户注册的视图'''
    if request.method=='GET':
        #这里把表单类的实例返回去是为了用验证码
        user_register_from=UserRegisterForm()
        return render(request,'register.html',{'user_register_form':user_register_from})
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
        return render(request,'login.html')
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
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请去您的邮箱激活您的账号,否则无法登录')
            #验证未通过
            else:
                return render(request,'login.html',{'msg':'邮箱或者密码有误'})
        #如果邮箱密码填写格式不对
        else:
            return render(request,'login.html',{'user_login_form':user_login_form})

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
                return render(request,'forgetpwd.html',{'msg':'用户不存在'})
        else:
            return render(request,'forgetpwd.html',{'user_forget_form':user_forget_form})

def user_reset(request,code):
    '''这是修改密码的视图'''
    if code:
        if request.method=='GET':
            return render(request,'password_reset.html',{'code':code})
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
                    return render(request,'password_reset.html',{'msg':'两次密码不一致','code':code})
            #如果用户输入的格式错误
            else:
                return render(request,'password_reset.html',{'user_reset_form':user_reset_form})

            






