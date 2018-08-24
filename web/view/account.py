from django.shortcuts import render, redirect, reverse, HttpResponse
from repository.models import *
from web.forms import *
from utils.check_code import create_validate_code
from io import BytesIO
import json


def check_code(request):
    f = BytesIO()
    img, code = create_validate_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


def register(request):
    if request.method == 'GET':
        obj = RegisterForm(request=request)
        return render(request, 'index/register.html', {'obj': obj})
    else:
        obj = RegisterForm(request=request, data=request.POST)
        if obj.is_valid():
            u = obj.cleaned_data.get('username')
            p = obj.cleaned_data.get('password')
            e = obj.cleaned_data.get('email')
            print(obj.cleaned_data)
            user = {
                'username': u,
                'pwd': p,
                'email': e,
            }
            User.objects.create(**user)
            return redirect('/')
        else:
            print(obj.errors)
            return render(request, 'index/register.html', {'obj': obj})


def login(request):
    if request.method == 'GET':
        obj = LoginForm(request=request)
        return render(request, 'index/login.html', {"obj": obj})
    else:
        result = {'status': False, 'message': None, 'data': None}
        obj = LoginForm(request=request, data=request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get('username')
            password = obj.cleaned_data.get('password')
            user = User.objects.filter(username=username, pwd=password).values(
                'username', 'nickname', 'pb__site', 'img', 'pb__id', 'email', 'id'
            ).first()
            if user:
                result['status'] = True
                request.session['user'] = user
                if obj.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                result['message'] = '用户名或密码错误'
        else:
            print(obj.errors)
            if 'check_code' in obj.errors:
                result['message'] = '验证码错误'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))


def logout(request):
    request.session.clear()
    return redirect('/')