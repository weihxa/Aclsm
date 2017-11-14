#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
import json
import models
import user_models
from django.core import serializers
from django.contrib.auth.hashers import make_password
from plugins.Decorators import admin_Auth,system_Auth
from froms import LoginForm
import datetime

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if  request.get_full_path() != '/' and request.get_full_path() != '/login/':
                    url = request.get_full_path().split('=')[1]
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponseRedirect('/index/')
            elif user is None:
                form = LoginForm()
                return render_to_response('login.html', RequestContext(request, {'form': form,'login_err': '您输入的用户名或密码错误,！'}))
            elif not user.is_active:
                form = LoginForm()
                return render_to_response('login.html',
                                          RequestContext(request, {'form': form, 'login_err': '账户被禁用！'}))
            else:
                form = LoginForm()
                return render_to_response('login.html',
                                          RequestContext(request, {'form': form, 'login_err': '未知异常，请联系管理员！'}))
        else:
            form = LoginForm()
            return render_to_response('login.html', RequestContext(request, {'form': form,}))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def checkpasswork(request):
    if request.method=='POST':
        try:
            oidpassword=request.POST.get('oldpassword')
            password=request.POST.get('password')
            user= auth.authenticate(username=str(request.user),password=oidpassword)
            user.set_password(password)
            user.save()
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/index/")
            return HttpResponseRedirect("/login/")
        except AttributeError,e:
            return HttpResponseRedirect("/login/")

@login_required
@system_Auth
def index(request,authoritys):
    return render(request, 'index.html',{"Authority": authoritys,},
                  context_instance=RequestContext(request))

@login_required
@admin_Auth
def users(request):
    if request.method == "POST":
        try:
            if request.POST.get('admin'):
                user = user_models.UserProfile.objects.create_user(email=request.POST.get('email'),username=request.POST.get('username'),password=request.POST.get('password'),admin=True)
            else:
                user = user_models.UserProfile.objects.create_user(email=request.POST.get('email'),username=request.POST.get('username'),password=request.POST.get('password'))
            user.save()
            return HttpResponseRedirect("/users/")
        except Exception,e:
            return HttpResponseRedirect("/users/")
    else:
        contact_list = user_models.UserProfile.objects.all()
        paginator = Paginator(contact_list, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'users.html',{"topics": contacts},
                      context_instance=RequestContext(request))

@login_required
@admin_Auth
def del_user(request):
    if request.method == "POST":
        user_models.UserProfile.objects.get(email=request.POST.get('modify')).delete()
        return HttpResponse(json.dumps('true'))

@login_required
def weekly(request):
    if request.method == 'GET':
        This_week =  models.Weekly.objects.filter(user_name__email=request.user.email).filter(create_date__gt=datetime.date.today()-datetime.timedelta(days=+datetime.date.today().isoweekday()))
        Last_week = models.Weekly.objects.filter(user_name__email=request.user.email).filter(create_date__lt=datetime.date.today()-datetime.timedelta(days=+datetime.date.today().isoweekday())).filter(create_date__gt=datetime.date.today()-datetime.timedelta(days=+datetime.date.today().isoweekday()+7))
        return render(request, 'weekly.html',{'This_week':This_week,'Last_week':Last_week},
                      context_instance=RequestContext(request))
    if request.method == 'POST':
        user = user_models.UserProfile.objects.get(email=request.user.email)
        models.Weekly.objects.create(user_name = user,
                                     weeklys = request.POST.get('weeklys'),
                                     workplan = request.POST.get('workplan'),
                                     completion = request.POST.get('completion'),
                                     coordination = request.POST.get('coordination'),
                                     nextweek = request.POST.get('nextweek')
                                     )
        return HttpResponseRedirect("/weekly/")

@login_required
def editweekly(request):
    weekly = models.Weekly.objects.get(id=request.POST.get('eweeklyid'))
    weekly.weeklys = request.POST.get('eweeklys')
    weekly.workplan = request.POST.get('eworkplan')
    weekly.completion = request.POST.get('ecompletion')
    weekly.coordination = request.POST.get('ecoordination')
    weekly.nextweek = request.POST.get('enextweek')
    weekly.save()
    return HttpResponseRedirect("/weekly/")

@login_required
def delweekly(request):
    if request.method == "POST":
        models.Weekly.objects.get(id=request.POST.get('modify')).delete()
        return HttpResponse(json.dumps('true'))

@login_required
def deparweekly(request):
    if request.method == 'GET':
        data = {}
        for i in user_models.UserProfile.objects.all():
            data2 = models.Weekly.objects.filter(user_name__email=i.email).filter(
            create_date__gt=datetime.date.today() - datetime.timedelta(days=+datetime.date.today().isoweekday()))
            data[i.username] = data2
        return render(request, 'deparweekly.html', {'data': data,'time':str(datetime.date.today() - datetime.timedelta(days=+datetime.date.today().isoweekday()))+'至'+str(datetime.date.today())},
                      context_instance=RequestContext(request))


@login_required
@admin_Auth
def gemail(request):
    if request.method == "GET":
        userget = user_models.UserProfile.objects.filter(email=request.GET.get('modify'))
        srvs_json = serializers.serialize("json", userget)
        print srvs_json
        return HttpResponse(srvs_json[1:-1])
    elif request.method == "POST":
        user = user_models.UserProfile.objects.get(email=request.POST.get('e_email'))
        user.username = request.POST.get('e_name')
        user.department = request.POST.get('e_department')
        user.mobile = request.POST.get('e_mobile')
        if request.POST.get('e_password').strip() != '':
            user.set_password=request.POST.get('e_password')
        if request.POST.get('e_admin') == None:
            user.is_admin = ''
        else:
            user.is_admin = 'True'
        if request.POST.get('e_active') == None:
            user.is_active = 'True'
        else:
            user.is_active = ''
        if len(request.POST.get('e_password')) != 0:
            user.password=make_password(request.POST.get('e_password'))
        user.save()
        if str(request.user) == request.POST.get('e_email') and len(request.POST.get('e_password')) != 0:
            user = auth.authenticate(username=str(request.user), password=request.POST.get('e_password'))
            auth.login(request, user)
        return HttpResponseRedirect("/users/")

@login_required
@admin_Auth
def authority(request):
    if request.method == "GET":
        user_list = user_models.UserProfile.objects.all().values('username')
        contact_list = models.Authoritys.objects.all()
        paginator = Paginator(contact_list, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'authority.html',{"topics": contacts,"user_list":user_list},
                      context_instance=RequestContext(request))
    elif request.method == "POST":
        try:
            user = user_models.UserProfile.objects.get(username=request.POST.get('username'))
            models.Authoritys.objects.get_or_create(user_name=user,mark=1,Auth_name=request.POST.get('system'))
            return HttpResponseRedirect("/authority/")
        except Exception, e:
            return HttpResponseRedirect("/authority/")

@login_required
@admin_Auth
def delauth(request):
    if request.method == "POST":
        models.Authoritys.objects.get(id=request.POST.get('modify')).delete()
        return HttpResponse(json.dumps('true'))
