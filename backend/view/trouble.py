from django.shortcuts import render, redirect, HttpResponse
from repository.models import *
from django.http import JsonResponse
from backend.auth import check_login
from utils.Pagination import Pager2
from backend.forms.article import *
from django.db.models import Q
from ..forms.trouble import *
import datetime
from django.db import connection


@check_login
def trouble(request):
    uid = request.session.get('user')['id']
    trouble_list = Trouble.objects.filter(user_id=uid).order_by('status')
    count = Trouble.objects.filter(user=uid).count()
    pagination = Pager2.Pagination(count, request.GET.get('p'), 10, 7)
    trouble_list = trouble_list[pagination.start():pagination.end()]
    base_url = '/backend/trouble'
    page_str = pagination.page_str(base_url)
    context = {
        'trouble_list': trouble_list,
        'page_str': page_str,
        'count': count,
    }
    return render(request, 'backend/trouble/backend_trouble.html', context=context)


@check_login
def add_trouble(request):
    uid = request.session.get('user')['id']
    dic = {}
    if request.method == 'GET':
        obj = TroubleAddForm()
        return render(request, 'backend/trouble/backend_add_trouble.html', {'obj': obj})
    elif request.method == 'POST':
        obj = TroubleAddForm(request.POST)
        if obj.is_valid():
            dic['status'] = 1
            dic['user_id'] = uid
            dic['create_time'] = datetime.datetime.now()
            dic.update(**obj.cleaned_data)
            Trouble.objects.create(**dic)
            return redirect('/backend/trouble')
        else:
            return render(request, 'backend/trouble/backend_add_trouble.html', {'obj': obj})
    else:
        return redirect('/backend/trouble')


@check_login
def edit_trouble(request, tid):
    uid = request.session.get('user')['id']
    if request.method == 'GET':
        trb = Trouble.objects.filter(status=1, id=tid).only('id', 'title', 'detail').first()
        if not trb:
            return render(request, 'backend/trouble/backend_no_trouble.html')
        obj = TroubleAddForm(initial={'title': trb.title, 'detail': trb.detail})
        return render(request, 'backend/trouble/backend_edit_trouble.html', {'obj': obj, 'tid': tid})
    else:
        obj = TroubleAddForm(request.POST)
        if obj.is_valid():
            v = Trouble.objects.filter(status=1, id=tid).update(**obj.cleaned_data)
            if not v:
                return render(request, 'backend/trouble/backend_no_trouble.html')
            else:
                return redirect('/backend/trouble')
        else:
            return render(request, 'backend/trouble/backend_edit_trouble.html', {'obj': obj, 'tid': tid})


def solve_trouble(request):
    uid = request.session.get('user')['id']
    count = Trouble.objects.filter(Q(status=1) | Q(handler=uid)).count()
    trouble_list = Trouble.objects.filter(Q(status=1) | Q(handler=uid)).order_by('status')
    pagination = Pager2.Pagination(count, request.GET.get('p'), 10, 7)
    trouble_list = trouble_list[pagination.start():pagination.end()]
    base_url = '/backend/solve-trouble'
    page_str = pagination.page_str(base_url)
    context = {
        'trouble_list': trouble_list,
        'count': count,
        'page_str': page_str,
    }
    return render(request, 'backend/trouble/backend_solve_trouble.html', context=context)


def trouble_solution(request, tid):
    uid = request.session.get('user')['id']
    if request.method == 'GET':
        count = Trouble.objects.filter(id=tid, handler=uid).count()
        if not count:
            v = Trouble.objects.filter(id=tid, status=1).update(status=2, handler=uid)
            if not v:
                return redirect('/backend/solve-trouble')
        trouble = Trouble.objects.filter(id=tid).first()
        obj = TroubleSolution(initial={'solution': trouble.solution})
        context = {
            'obj': obj,
            'tid': tid,
            'trouble': trouble,
        }
        return render(request, 'backend/trouble/backend_solution_trouble.html', context=context)
    else:
        ret = Trouble.objects.filter(handler=uid, status=2, id=tid).count()
        if not ret:
            return HttpResponse('去你妈的')
        obj = TroubleSolution(request.POST)
        dic = {}
        if obj.is_valid():
            dic['solve_time'] = datetime.datetime.now()
            dic['solution'] = obj.cleaned_data.get('solution')
            dic['status'] = 3
            Trouble.objects.filter(id=tid, handler=uid, status=2).update(**dic)
            return redirect('/backend/solve-trouble')
        trouble = Trouble.objects.filter(id=tid).first()
        context = {
            'obj': obj,
            'tid': tid,
            'trouble': trouble,
        }
        return render(request, 'backend/trouble/backend_solution_trouble.html', context=context)


def solution_view(request, tid):
    trouble = Trouble.objects.filter(id=tid).first()
    if request.method == 'GET':
        obj = SolutionEvaluate()
        return render(request, 'backend/trouble/backend_solution_view.html',
                      {'trouble': trouble, 'obj': obj, 'tid': tid})
    else:
        obj = SolutionEvaluate(request.POST)
        if obj.is_valid():
            Trouble.objects.filter(id=tid, status=3).update(**obj.cleaned_data)
            return redirect('/backend/trouble')
        else:
            return render(request, 'backend/trouble/backend_solution_view.html',
                          {'trouble': trouble, 'obj': obj, 'tid': tid})


def trouble_table(request):
    trouble_list = Trouble.objects.all()
    return render(request, 'backend/trouble/backend_trouble_table.html', {'trouble_list': trouble_list})


def trouble_table_json(request):
    user_list = User.objects.filter()
    response = []
    for user in user_list:
        cursor = connection.cursor()
        cursor.execute(
            """select strftime('%%s',strftime("%%Y-%%m-01",create_time)) * 1000,count(id) from Trouble where handler_id = %s group by strftime("%%Y-%%m",create_time)""",
            [user.id, ])
        result = cursor.fetchall()
        temp = {
            'name': user.username,
            'data': result
        }
        response.append(temp)
    import json
    return HttpResponse(json.dumps(response))

