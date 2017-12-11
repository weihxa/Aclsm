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
from SCMS import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index, name='index'),
    url(r'^help/$', views.help, name='help'),
    url(r'^pcmanager/', views.pcmanager, name='pcmanager'),
    url(r'^adddevice/', views.adddevice, name='adddevice'),
    url(r'^deldevice/', views.deldevice, name='deldevice'),
    url(r'^groupmodify/', views.groupmodify, name='groupmodify'),
    url(r'^delgroup/', views.delgroup, name='delgroup'),
    url(r'^editgroup/', views.editgroup, name='editgroup'),
    url(r'^confile/', views.confile, name='confile'),
    url(r'^delconf/', views.delconf, name='delconf'),
    url(r'^editconf/', views.editconf, name='editconf'),
    url(r'^page/', views.page, name='page'),
    url(r'^delpage/', views.delpage, name='delpage'),
    url(r'^nginxpush/', views.nginxpush, name='nginxpush'),
    url(r'^tomcatpush/', views.tomcatpush, name='tomcatpush'),
    url(r'^nginxinstall/', views.nginxinstall, name='nginxinstall'),
    url(r'^tomcatinstall/', views.tomcatinstall, name='tomcatinstall'),
    url(r'^generate/', views.generate, name='generate'),
    url(r'^tables/', views.tasks_tables, name='tasks_tables'),
    url(r'^playbook/', views.playbook, name='playbook'),
    url(r'^playbook_upload/', views.playbook_upload, name='playbook_upload'),
    url(r'^cmdrun/', views.cmdrun, name='cmdrun'),
    # url(r'^filepush/', views.filepush,name='filepush'),

]
