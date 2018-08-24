from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from repository.models import *
from utils.Pagination.Pager import *
from web.forms import *
from utils.Pagination import Pager2
import os
from django.db.models import F


def index(request, *args, **kwargs):
    article_type_list = BlogArticle.type_choices
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'

    count = BlogArticle.objects.filter(**kwargs).count()
    pagination = Pagination(count, request.GET.get('p'), 6, 7)
    articles = BlogArticle.objects.filter(**kwargs).order_by('-add_date')
    articles = articles[pagination.start():pagination.end()]
    page_str = pagination.page_str(base_url)

    context = {
        'articles': articles,
        'page_str': page_str,
        'article_type_list': article_type_list,
        'article_type_id': article_type_id,
    }
    return render(request, 'index/index.html', context=context)


def readCount(request):
    ret = {'status':True, 'message': None}
    try:
        aid = request.POST.get('aid')
        art = BlogArticle.objects.get(id=aid)
        art.read_count = F('read_count')+1
        art.save()
    except Exception as e:
        print(e)
        ret['message'] = 'error'
    return JsonResponse(ret)


def home(request, *args, **kwargs):
    site = kwargs['site']
    blog = PersonalBlog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')
    bid = PersonalBlog.objects.filter(site=site).values('id').first()
    bid = bid['id']
    tags = ArticleTag.objects.filter(blog_id=bid).all()
    classifies = ArticleClassify.objects.filter(blog_id=bid).all()
    ctime = BlogArticle.objects.raw(
        'select id, count(id) as num,strftime("%%Y-%%m",add_date) as ctime from BlogArticle where blog_id=%s group by strftime("%%Y-%%m",add_date) order by strftime("%%Y-%%m",add_date) desc  ',
        [bid])
    article_list = BlogArticle.objects.filter(blog_id=bid).order_by('-add_date').all()
    context = {
        'blog': blog,
        'tags': tags,
        'classifies': classifies,
        'ctime': ctime,
        'article_list': article_list
    }
    return render(request, 'home/home_article_list.html', context=context)


def filters(request, condition, site, num):
    blog = PersonalBlog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')
    blog = PersonalBlog.objects.filter(site=site).first()
    bid = PersonalBlog.objects.filter(site=site).values('id').first()
    bid = bid['id']
    tags = ArticleTag.objects.filter(blog_id=bid).all()
    classifies = ArticleClassify.objects.filter(blog_id=bid).all()
    ctime = BlogArticle.objects.raw(
        'select id, count(id) as num,strftime("%%Y-%%m",add_date) as ctime from BlogArticle where blog_id=%s group by strftime("%%Y-%%m",add_date) order by strftime("%%Y-%%m",add_date) desc  ',
        [bid])
    if condition == 'tag':
        article_list = BlogArticle.objects.filter(tags=num, blog_id=bid).all()
    elif condition == 'classify':
        article_list = BlogArticle.objects.filter(classify=num, blog_id=bid).all()
    elif condition == 'date':
        article_list = BlogArticle.objects.filter(blog_id=bid).extra(
            where=['strftime("%%Y-%%m",add_date)=%s'], params=[num, ]).all()
    else:
        article_list = []
    context = {
        'blog': blog,
        'tags': tags,
        'classifies': classifies,
        'ctime': ctime,
        'article_list': article_list,
    }
    return render(request, 'home/home_article_list.html', context=context)


def detail(request, site, aid):
    blog = PersonalBlog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')
    bid = PersonalBlog.objects.filter(site=site).values('id').first()
    bid = bid['id']
    tags = ArticleTag.objects.filter(blog_id=bid).all()
    classifies = ArticleClassify.objects.filter(blog_id=bid).all()
    ctime = BlogArticle.objects.raw(
        'select id, count(id) as num,strftime("%%Y-%%m",add_date) as ctime from BlogArticle where blog_id=%s group by strftime("%%Y-%%m",add_date) order by strftime("%%Y-%%m",add_date) desc  ',
        [bid])
    article_detail = BlogArticle.objects.filter(id=aid).first()
    user = User.objects.filter(pb__site=site).first()
    comments = ArticleComment.objects.filter(bid=aid).all().order_by('-create_time')
    count = ArticleComment.objects.filter(bid=aid).count()
    pagination = Pager2.Pagination(count, request.GET.get('p'), 5, 7)
    comments = comments[pagination.start():pagination.end()]
    base_url = '/' + site + '/' + aid
    page_str = pagination.page_str(base_url)
    context = {
        'blog': blog,
        'tags': tags,
        'classifies': classifies,
        'ctime': ctime,
        'article_detail': article_detail,
        'user': user,
        'comments': comments,
        'page_str': page_str,
    }
    return render(request, 'home/home_detail.html', context=context)


def upload(request):
    ret = {'error': None, 'url': None, 'message':None}
    if request.FILES:
        img = request.FILES.get('img')
        ret['error'] = 0
    file_path = os.path.join('static/comment_img', img.name)
    with open(file_path, 'wb') as f:
        for line in img.chunks():
            f.write(line)
    ret['url'] = '/' + file_path
    return JsonResponse(ret)


def comment(request):
    ret = {'status': True, 'data': None}
    content = request.POST.get('comment')
    uid = request.POST.get('user')
    aid = request.POST.get('aid')
    rid = request.POST.get('rid')
    new_comment = {
        'content': content,
        'bid_id': aid,
        'uid_id': uid,
        'reply_id': rid,
    }
    ArticleComment.objects.create(**new_comment)
    return JsonResponse(ret)


def updown(request):
    ret = {'status': False, 'data': None, 'message': None}
    uid = request.POST.get('uid')
    aid = request.POST.get('aid')
    article_status = int(request.POST.get('updown'))
    article_up_down = {
        'uid_id': uid,
        'aid_id': aid,
        'status': article_status,
    }
    try:
        s = ArticleStatus.objects.create(**article_up_down)
        if s:
            count = BlogArticle.objects.get(id=aid)
            if article_status == 0:
                count.up_count = F('up_count') + 1
                count.save()
            else:
                count.down_count = F('down_count') + 1
                count.save()
            ret['status'] = True
            ret['message'] = 'success'
    except Exception as e:
        ret['message'] = '你已经赞/踩过了'
    return JsonResponse(ret)
