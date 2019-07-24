from django.shortcuts import redirect,reverse
from django.http import JsonResponse

def login_decorator(func):
    '''这是登录装饰器'''
    def inner(request,*args,**kwargs):
        #如果已经登录了，就按原来的走
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            #用户在没登录的时候也不可以收藏，这属于ajax请求，先判断一下
            if request.is_ajax():
                print('是ajax')
                #ajax请求是不支持redirect的，所以我们只能返回json
                return JsonResponse({'status':'nologin'})

            #完整的url也保存在request里面，我们先拿到
            url=request.get_full_path()
            #把当前的url(也就是我们希望登录后还回到的地方)保存在登录页面的cookie里面
            #点击登录按钮之后，根据cookie里存放的urL决定往哪里跳转
            ret=redirect(reverse('users:user_login'))
            ret.set_cookie('url',url)
            return ret


    return inner

