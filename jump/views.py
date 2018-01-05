#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect,StreamingHttpResponse
from django.contrib import auth
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from Integrated.plugins.Decorators import Perm_verification
import json
import models,code




@login_required
@Perm_verification(perm='jump')
def index(request):
    return render(request, 'jump/index.html',
                      context_instance=RequestContext(request))


@login_required
@Perm_verification(perm='jump')
def lists(request):
    return render(request, 'jump/lists.html',
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