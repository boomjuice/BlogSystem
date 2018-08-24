from django.forms import fields
from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from repository.models import *


class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)


class RegisterForm(BaseForm, forms.Form):
    username = fields.CharField(max_length=20, min_length=8,
                                error_messages={
                                    'required': '用户名不能为空',
                                    'max_length': '用户名多于20个字符',
                                    'min_length': '用户名少于8个字符', })
    password = fields.RegexField(
        regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$,\/\%\^\&\*\(\)\.])[0-9a-zA-Z!@#$\%\^\&\*\(\)\.,\/]{8,16}$',
        min_length=8,
        max_length=16,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于16字符"})
    confirm_pwd = fields.CharField()
    email = fields.EmailField(error_messages={
        'required': '邮箱不能为空',
        'invalid': '邮箱格式错误',
    })
    check_code = fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code(self):
        if self.request.session['check_code'].upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

    def clean_email(self):
        e = self.cleaned_data.get('email')
        if User.objects.filter(email=e):
            raise ValidationError(message='该邮箱已经注册过了', code='invalid')
        else:
            return e

    def clean(self):
        v1 = self.cleaned_data.get('password')
        v2 = self.cleaned_data.get('confirm_pwd')
        if v1 == v2:
            pass
        else:
            raise ValidationError('密码输入不一致')


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField()
    password = fields.CharField()
    check_code = fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )
    rmb = fields.IntegerField(required=False)

    def clean_check_code(self):
        if self.request.session['check_code'].upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')
