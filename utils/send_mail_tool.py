from users.models import EmailVerifyCode
import random
from django.core.mail import send_mail
from guliedu.settings import EMAIL_FROM

def get_random_code(code_length):
    '''生成随机验证码'''
    code_source='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code=''
    for i in range(code_length):
        #随机选择一个字符，拼接到code上面
        letter=random.choice(code_source)
        code+=letter
    return code


def send_email_code(email,send_type):
    '''这是发送邮箱验证码的函数'''
    #第一步：创建验证码，存到数据库，后面用来比对
    code=get_random_code(8)
    evc=EmailVerifyCode()
    evc.email=email
    evc.send_type=send_type
    evc.code=code
    evc.save()
    #第二步：发邮件
    send_title=''
    send_body=''
    if send_type==1:
        send_title='欢迎注册谷粒教育'
        send_body='请点击以下链接激活您的账号:\nhttp://127.0.0.1:8000/users/user_active/'+code
        send_mail(send_title,send_body,EMAIL_FROM,[email])
    if send_type==2:
        send_title='谷粒教育重置密码'
        send_body='请点击以下链接重置您的密码：\nhttp://127.0.0.1:8000/users/user_reset/'+code
        send_mail(send_title,send_body,EMAIL_FROM,[email])
    if send_type==3:
        send_title='谷粒教育修改邮箱验证码'
        send_body='下面是您的验证码(5分钟内有效)：\n'+code
        send_mail(send_title,send_body,EMAIL_FROM,[email])

