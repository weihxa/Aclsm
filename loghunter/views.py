#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from Integrated.plugins.Decorators import Perm_verification
import json
from django.views.decorators.csrf import csrf_exempt
import core
import models

@login_required
@Perm_verification(perm='logs')
def index(request):
    containerd = core.index()
    return render(request, 'loghunter/index.html',{"containerd": containerd},
                      context_instance=RequestContext(request))


def earlywarn(request):
    return render(request, 'loghunter/earlywarn.html',
                      context_instance=RequestContext(request))

@csrf_exempt
def report(request):
    if request.method == "POST":
        logs = core.report(request)
        return HttpResponse(json.dumps(logs))
    elif request.method == "GET":
        return HttpResponse(json.dumps({'error':'only post'}))

def get_report(request):
    data_list = core.get_report()
    return  HttpResponse(json.dumps({'data':data_list}))


def detail_report(request):
    if request.method == 'GET':
        return render(request, 'loghunter/detailearly.html',{"ipaddress": request.GET.get('ip')},
                      context_instance=RequestContext(request))

def deldevall(request):
    models.Early_warn.objects.all().delete()
    return HttpResponse(json.dumps('true'))

def getdeatil(request):
    data_list = core.get_deatil(request.POST.get('modify'))
    return HttpResponse(json.dumps({'data': data_list}))


def detaillogs(request):
    data = core.get_deatil_logs(request.GET.get('modify'))
    return HttpResponse(json.dumps(data))


def disks(request):
    normal,unusual = core.get_disk()
    try:
        date = models.disk.objects.all()[0]
        a_time = date.create_date
    except IndexError,e:
        a_time = '暂无数据'
    return render(request, 'loghunter/disks.html',{'normal':normal,'unusual':unusual,'datetime':a_time},
                      context_instance=RequestContext(request))