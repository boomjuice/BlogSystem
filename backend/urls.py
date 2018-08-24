"""保障系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from backend.view import user
from backend.view import trouble

urlpatterns = [
    url(r'^index$', user.index, name='index'),
    url(r'^article-(?P<article_type_id>\w+)-(?P<classify_id>\w+)$', user.article, name='article'),
    url(r'^add-article$', user.add_article),
    url(r'^del-article$', user.del_article),
    url(r'^edit-article/(?P<aid>\d+)$', user.edit_article),
    url(r'^trouble$', trouble.trouble),
    url(r'^add-trouble$', trouble.add_trouble),
    url(r'^edit-trouble/(?P<tid>\d+)$', trouble.edit_trouble),
    url(r'^solve-trouble$', trouble.solve_trouble),
    url(r'^solve-trouble/(?P<tid>\d+)$', trouble.trouble_solution),
    url(r'^solution-view/(?P<tid>\d+)$', trouble.solution_view),
    url(r'^trouble-table$', trouble.trouble_table),
    url(r'^trouble-table-json$', trouble.trouble_table_json),

]
