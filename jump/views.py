#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect,StreamingHttpResponse
from django.contrib import auth
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from Integrated.plugins.Decorators import Perm_verification
from django.core import serializers
import json
import models,code,tasks




@login_required
@Perm_verification(perm='jump')
def index(request):
    return render(request, 'jump/index.html',
                      context_instance=RequestContext(request))


@login_required
@Perm_verification(perm='jump')
def lists(request):
    print request.user
    if request.method == "GET":
        if not request.user.is_admin:
            pass
        else:
            data = models.Jump_prem.objects.filter(username__username=request.user)
            print data[0].group
            data2 = models.Jump_group.objects.filter(groupname=data[0].group)
        return render(request, 'jump/lists.html',{'devlist':data2[0].dev_list.split(','),'group':data[0].group},
                          context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jump')
def users(request):
    if request.method == "GET":
        data = models.Jump_user.objects.all()
        return render(request, 'jump/users.html',{'data':data},
                          context_instance=RequestContext(request))
    elif request.method == "POST":
        data = code.jumpuser_post(request)
        return HttpResponse(json.dumps(data))


@login_required
@Perm_verification(perm='jump')
def deluser(request):
    models.Jump_user.objects.filter(id=request.POST.get('modify')).delete()
    return HttpResponse(json.dumps('true'))


@login_required
@Perm_verification(perm='jump')
def edit_users(request):
    data = code.jumpuser_edit(request)
    return HttpResponse(json.dumps(data))

@login_required
@Perm_verification(perm='jump')
def group(request):
    if request.method == "GET":
        group_data,user_data,dev_data = code.group_data(request)
        return render(request, 'jump/group.html',{'group_data':group_data,'user_data':user_data,'dev_data':dev_data},
                      context_instance=RequestContext(request))
    elif request.method == "POST":
        data = code.group_post(request)
        return HttpResponse(json.dumps(data))

@login_required
@Perm_verification(perm='jump')
def delgroup(request):
    models.Jump_group.objects.filter(id=request.POST.get('modify')).delete()
    return HttpResponse(json.dumps('true'))


@login_required
@Perm_verification(perm='jump')
def edit_group(request):
    data = code.group_edit(request)
    return HttpResponse(json.dumps(data))


@login_required
@Perm_verification(perm='jump')
def prem(request):
    if request.method == "GET":
        prem_data, group_data, sys_user = code.prem_data(request)
        return render(request, 'jump/prem.html',{'prem_data':prem_data,'group_data':group_data,'sys_user':sys_user},
                      context_instance=RequestContext(request))
    elif request.method == "POST":
        data = code.prem_post(request)
        return HttpResponse(json.dumps(data))

@login_required
@Perm_verification(perm='jump')
def delprem(request):
    models.Jump_prem.objects.filter(id=request.POST.get('modify')).delete()
    return HttpResponse(json.dumps('true'))


@login_required
@Perm_verification(perm='jump')
def edit_prem(request):
    data = code.edit_prem(request)
    return HttpResponse(json.dumps(data))


@login_required
@Perm_verification(perm='jump')
def push_group(request):
    if request.method == "POST":
        tasks.push_prem.delay(request.POST.get('modify'))
        return HttpResponse(json.dumps('true'))

@login_required
@Perm_verification(perm='jump')
def get_notice_list(request):
    if request.method == "POST":
        models.Jump_Notice.objects.filter(status=1).update(status=0)
        return HttpResponse(True)
    else:
        data = models.Jump_Notice.objects.filter(status=1)
        srvs_json = serializers.serialize("json", data)
        return HttpResponse(srvs_json)

@login_required
@Perm_verification(perm='jump')
def get_notice_num(request):
    num = models.Jump_Notice.objects.filter(status=1).count()
    return HttpResponse(num)