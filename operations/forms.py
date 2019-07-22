from django import forms
from . models import UserAsk,UserComment
import re

#ModelForm比Form还高级,不需要单独写验证规则，直接用model的规则就行了
class UserAskForm(forms.ModelForm):
    '''这是用户咨询表单类'''
    class Meta:
        model=UserAsk
        fields=['name','course','phone']
        #如果用到了所有字段，就写fileds='__all__'
        #如果用到了大部分字段，就写exclude=['add_time]，就是说除了列表里的，其他都要
    
    def clean_phone(self):
        '''这是自定义的对手机号的进一步验证'''
        phone=self.cleaned_data['phone']
        com=re.compile(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$')
        if com.match(phone):
            return phone
        #如果手机号不合法，就抛出异常
        else:
            raise forms.ValidationError('手机号码不合法')

class UserCommentForm(forms.ModelForm):
    '''这是用户评论的表单类'''
    class Meta:
        model=UserComment
        fields=['comment_content']
    def clean_course_id(self):
        '''这个用于验证传过来的课程id是否合法'''
        comment_course_id=self.cleaned_data['comment_course_id']
        com=re.compile(r'^\d+$')
        if com.match(course_id):
            return comment_course_id
        else:
            return forms.ValidationError('课程id不合法') 