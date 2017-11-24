#-*- coding:utf-8 -*-
"""xbman-Integrated URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from loghunter import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index, name='index'),
    url(r'^earlywarn/$', views.earlywarn, name='earlywarn'),
    url(r'^report/$', views.report, name='report'),
    url(r'^getreport/$', views.get_report, name='get_list'),
    url(r'^detailreport/$', views.detail_report, name='detail_list'),
    url(r'^getdetail/$', views.getdeatil, name='getdeatil'),
    url(r'^detaillogs/$', views.detaillogs, name='detaillogs'),
    url(r'^deldevall/$', views.deldevall, name='deldevall'),
    url(r'^disks/$', views.disks, name='disks'),

]
