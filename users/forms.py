from django import forms
from captcha.fields import CaptchaField
from . models import UserProfile

class UserRegisterForm(forms.Form):
    '''这是用户注册表单类'''
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=3,max_length=15,
    error_messages={
    'required':'密码必须填写',
    'min_length':'密码至少3位',
    'max_length':'密码不能超过15位'})
    #下面这个字段是验证码
    captcha=CaptchaField()


class UserLoginForm(forms.Form):
    '''这是用户登录表单类'''
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=3,max_length=15,
    error_messages={
    'required':'密码必须填写',
    'min_length':'密码至少3位',
    'max_length':'密码不能超过15位'})

class UserForgetForm(forms.Form):
    '''这是用户忘记密码的表单类'''
    email=forms.EmailField(required=True)
    #下面这个字段是验证码
    captcha=CaptchaField()

class UserResetForm(forms.Form):
    '''这是用户修改密码的表单类'''
    password=forms.CharField(required=True,min_length=3,max_length=15,
    error_messages={
    'required':'密码必须填写',
    'min_length':'密码至少3位',
    'max_length':'密码不能超过15位'})
    password1=forms.CharField(required=True,min_length=3,max_length=15,
    error_messages={
    'required':'密码必须填写',
    'min_length':'密码至少3位',
    'max_length':'密码不能超过15位'})

class UserChangeimageForm(forms.ModelForm):
    '''这是用户修改头像的表单类'''
    class Meta:
        model = UserProfile
        fields=['image']

class UserChangeinfoForm(forms.ModelForm):
    '''这是用户修改普通信息的表单类'''
    class Meta:
        model=UserProfile
        fields=['nickname','birthday','gender','address','phone']

