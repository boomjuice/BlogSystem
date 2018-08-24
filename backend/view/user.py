from django.shortcuts import render, redirect
from repository.models import *
from django.http import JsonResponse
from backend.auth import check_login
from utils.Pagination import Pager2
from backend.forms.article import *
from django.db import transaction


@check_login
def index(request):
    return render(request, 'backend/backend_index.html')


@check_login
def article(request, *args, **kwargs):
    condition = {}
    url = {}
    bid = request.session.get('user')['pb__id']
    for k, v in kwargs.items():
        temp = int(v)
        kwargs[k] = temp
        url[k] = v
        if int(v) == 0:
            pass
        else:
            condition[k] = v
    condition['blog_id'] = bid
    base_url = '/backend/article' + '-' + url['article_type_id'] + '-' + url['classify_id']
    article_list = BlogArticle.objects.filter(**condition).all().order_by('-add_date')
    count = BlogArticle.objects.filter(**condition).count()
    types = BlogArticle.type_choices
    classify_list = ArticleClassify.objects.filter(blog_id=bid)
    pagination = Pager2.Pagination(count, request.GET.get('p'), 5, 5)
    article_list = article_list[pagination.start():pagination.end()]
    page_str = pagination.page_str(base_url)
    context = {
        'count': count,
        'types': types,
        'classify_list': classify_list,
        'article_list': article_list,
        'condition': condition,
        'kwargs': kwargs,
        'page_str': page_str,
    }
    return render(request, 'backend/article/backend_article.html', context=context)


@check_login
def add_article(request):
    if request.method == 'GET':
        obj = ArticleForm(request=request)
        return render(request, 'backend/article/backend_add_article.html', {'obj': obj})
    elif request.method == 'POST':
        obj = ArticleForm(request=request, data=request.POST)
        if obj.is_valid():
            with transaction.atomic():
                tags = obj.cleaned_data.pop('tags')
                content = obj.cleaned_data.pop('content')
                obj.cleaned_data['blog_id'] = request.session.get('user')['pb__id']
                aid = BlogArticle.objects.create(**obj.cleaned_data)
                BlogArticleDetail.objects.create(content=content, bid=aid)
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(TagsToArticle(article_id=aid.id, tag_id=tag_id))
                TagsToArticle.objects.bulk_create(tag_list)
                return redirect('/backend/article-0-0')
        else:
            return render(request, 'backend/article/backend_add_article.html', {'obj': obj})
    else:
        return redirect('/')


@check_login
def del_article(request):
    ret = {'status': False, 'message': None}
    aid = request.POST.get('aid')
    try:
        BlogArticle.objects.filter(id=aid).delete()
        BlogArticleDetail.objects.filter(bid=aid).delete()
        ret['status'] = True
        return JsonResponse(ret)
    except Exception as e:
        ret['message'] = e
        return JsonResponse(ret)


@check_login
def edit_article(request, aid):
    bid = request.session.get('user')['pb__id']
    if request.method == 'GET':
        art = BlogArticle.objects.filter(blog_id=bid, id=aid).first()
        if not art:
            return render(request, 'backend/article/backend_no_article.html')
        content = BlogArticleDetail.objects.filter(bid=aid).first()
        if not content:
            BlogArticleDetail.objects.create(bid_id=art.id)
        content = BlogArticleDetail.objects.filter(bid=aid).first()
        tags = art.tags.values_list('id')
        if tags:
            tags = list(zip(*tags))[0]
        context = {
            'aid': art.id,
            'title': art.title,
            'summary': art.summary,
            'content': content.content,
            'article_type_id': art.article_type_id,
            'classify_id': art.classify_id,
            'tags': tags,
        }
        obj = ArticleForm(request=request, initial=context)
        return render(request, 'backend/article/backend_edit_article.html', {'obj': obj, 'aid': aid})
    elif request.method == 'POST':
        obj = ArticleForm(request=request, data=request.POST)
        if obj.is_valid():
            art = BlogArticle.objects.filter(blog_id=bid, id=aid).first()
            if not art:
                return render(request, 'backend/article/backend_no_article.html')
            with transaction.atomic():
                tags = obj.cleaned_data.pop('tags')
                content = obj.cleaned_data.pop('content')
                BlogArticle.objects.filter(blog_id=bid,id=aid).update(**obj.cleaned_data)
                BlogArticleDetail.objects.filter(bid=aid).update(content=content)
                TagsToArticle.objects.filter(article=aid).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(TagsToArticle(article_id=aid, tag_id=tag_id))
                TagsToArticle.objects.bulk_create(tag_list)
                return redirect('/backend/article-0-0')
        else:
            return render(request, 'backend/article/backend_add_article.html', {'obj': obj})
    else:
        return redirect('/')
