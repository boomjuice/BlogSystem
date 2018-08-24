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
from django.contrib import admin
from web.view import views as vs
from web.view import account as ac

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', vs.index),
    url(r'^all/(?P<article_type_id>(\d+))$', vs.index, name='index'),
    url(r'^register$', ac.register, name='register'),
    url(r'^checkcode', ac.check_code, name='check_code'),
    url(r'^login$', ac.login, name='login'),
    url(r'^logout$', ac.logout, name='logout'),
    url(r'^read$', vs.readCount),
    url(r'^updown$',vs.updown,),
    url(r'^upload$', vs.upload, name='upload'),
    url(r'^comment$', vs.comment),
    url(r'^(?P<site>\w+)$', vs.home, name='home'),
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(classify)))/(?P<num>\w+-*\w*)$', vs.filters, name='filters'),
    url(r'^(?P<site>\w+)/(?P<aid>\w+)', vs.detail, name='detail'),

]
