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
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index, name='jump-index'),
    url(r'^lists/$', views.lists, name='jump-lists'),
    url(r'^users/$', views.users, name='jump-users'),
    url(r'^deluser/$', views.deluser, name='jump-deluser'),
    url(r'^edit_users/$', views.edit_users, name='jump-edit_users'),
    url(r'^group/$', views.group, name='jump-group'),
    url(r'^delgroup/$', views.delgroup, name='jump-delgroup'),
    url(r'^edit_group/$', views.edit_group, name='jump-edit_group'),
    url(r'^prem/$', views.prem, name='jump-prem'),
    url(r'^delprem/$', views.delprem, name='jump-delprem'),
    url(r'^edit_prem/$', views.edit_prem, name='jump-edit_prem'),
    url(r'^push_group/$', views.push_group, name='jump-push_group'),

]
