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
from Integrated import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', views.login),
    url(r'^login/$', views.login,name='login'),
    url(r'^index/$', views.index,name='index'),
    url(r'^checkpasswork/', views.checkpasswork,name='checkpasswork'),
    url(r'^logout/', views.logout,name='logout'),
    url(r'^users/', views.users,name='uses'),
    url(r'^deluser/', views.del_user,name='deluser'),
    url(r'^gemail/', views.gemail,name='gemail'),
    url(r'^authority/', views.authority,name='authority'),
    url(r'^delauth/', views.delauth,name='delauth'),
    url(r'^weekly/', views.weekly,name='weekly'),
    url(r'^delweekly/', views.delweekly,name='delweekly'),
    url(r'^editweekly/', views.editweekly,name='editweekly'),
    url(r'^deparweekly/', views.deparweekly,name='deparweekly'),
    # url(r'^releases/', include('releases.urls')),
    # url(r'^scms/', include('SCMS.urls')),
    url(r'^loghunter/', include('loghunter.urls')),
    url(r'^asset/',include('asset.urls')),

]
