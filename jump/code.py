#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
import models
import cryption
from SCMS import models as scms_models
from Integrated import user_models
from django.db.models import Count,Max
import datetime
import os

def index():
    containerd = {}
    containerd['user'] = models.Jump_user.objects.all().count()
    containerd['group'] = models.Jump_group.objects.all().count()
    containerd['prem'] = models.Jump_prem.objects.all().count()
    list_tup = []
    for i in range(1,31):
        sys_list = []
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-int(i))
        n_days = now + delta
        data = models.Jump_logs.objects.filter(create_date__year=n_days.strftime('%Y')).filter(create_date__month=n_days.strftime('%m')).filter(
            create_date__day=n_days.strftime('%d')).count()
        sys_list.append(str(n_days.strftime('%Y-%m-%d')))
        sys_list.append(data)
        list_tup.append(sys_list)
    list_tup.reverse()
    containerd['syslist'] = (list_tup)
    max_ip = models.Jump_logs.objects.values('ipaddress').annotate(counts=Count('ipaddress')).latest('counts')
    containerd['max_ip'] = max_ip
    max_user = models.Jump_logs.objects.values('username__username').annotate(counts=Count('username')).latest('counts')
    containerd['max_user'] = max_user
    try:
        disk = os.statvfs("/")
        available = disk.f_bsize * disk.f_bavail/1024/1024/1024
        containerd['available'] = available
    except AttributeError,e:
        containerd['available'] = '获取失败'
    return containerd

def jumpuser_post(request):
    try:
        if  models.Jump_user.objects.filter(username=request.POST.get('username')):
            return (False,'系统账号重复！请检查！')
        else:
            models.Jump_user.objects.create(username=request.POST.get('username'),
                                            permiss=request.POST.get('description'),
                                            password=cryption.encryption(str(request.POST.get('u_password'))))
            return (True, '系统账号创建成功')
    except Exception,e:
        print e
        return (False, '未知错误，请刷新页面后尝试')

def jumpuser_edit(request):
    try:
        if request.POST.get('e_password'):
            models.Jump_user.objects.filter(id=request.POST.get('userid')).update(
                permiss=request.POST.get('e_description'),password=cryption.encryption(str(request.POST.get('e_password'))))
        else:
            models.Jump_user.objects.filter(id=request.POST.get('userid')).update(permiss=request.POST.get('e_description'))
        return (True, '修改成功')
    except Exception,e:
        print e
        return (False, '未知错误，请刷新页面后尝试')

def group_data(request):
    group_data = models.Jump_group.objects.all()
    user_data = models.Jump_user.objects.all()
    dev_data = scms_models.device_config.objects.all()
    return (group_data,user_data,dev_data)


def group_post(request):
    try:
        if  models.Jump_group.objects.filter(groupname=request.POST.get('groupname')):
            return (False,'组账号重复！请检查！')
        else:
            user = models.Jump_user.objects.get(id=request.POST.get('username'))
            models.Jump_group.objects.create(groupname=request.POST.get('groupname'),
                                             user=user,
                                             dev_list=','.join(request.POST.getlist('pclist')))
            return (True, '组账号创建成功')
    except Exception,e:
        print e
        return (False, '未知错误，请刷新页面后尝试')

def group_edit(request):
    try:
        user = models.Jump_user.objects.get(id=request.POST.get('e_username'))
        models.Jump_group.objects.filter(id=request.POST.get('groupid')).update(
                                         user=user,
                                         dev_list=','.join(request.POST.getlist('e_pclist')))
        return (True, '修改成功')
    except Exception,e:
        print e
        return (False, '未知错误，请刷新页面后尝试')


def prem_data(request):
    prem_data = models.Jump_prem.objects.all()
    group_data = models.Jump_group.objects.all()
    sys_user = user_models.UserProfile.objects.all()
    return (prem_data,group_data,sys_user)

def prem_post(request):
    try:
        if  models.Jump_prem.objects.filter(username__username=request.POST.get('username')):
            return (False,'用户权限已绑定,请确认！')
        else:
            user = user_models.UserProfile.objects.get(username=request.POST.get('username'))
            group = models.Jump_group.objects.get(id=request.POST.get('group'))
            models.Jump_prem.objects.create(username=user,
                                            group=group)
            return (True, '权限绑定成功！')
    except Exception,e:
        print e
        return (False, '未知错误，请刷新页面后尝试')

def edit_prem(request):
    try:
        group = models.Jump_group.objects.get(id=request.POST.get('e_groupname'))
        models.Jump_prem.objects.filter(id=request.POST.get('permid')).update(
                                         group=group)
        return (True, '修改成功')
    except Exception,e:
        print e
        return (False, '未知错误，请刷新页面后尝试')

def loglist_data(request):
    loglist = models.Jump_logs.objects.filter(username=request.user)
    return loglist

def get_deatil_logs(request):
    try:
        logs = models.Jump_logs.objects.filter(id=request.GET.get('modify'))
        with open(logs[0].file_path,'r') as files:
            data = files.read()
        return data
    except Exception,e:
        return '服务端发生未知错误！或日志文件不存在！'

def all_loglist(request):
    data = models.Jump_logs.objects.values('username__username').annotate(counts=Count('ipaddress'),dtime=Max('create_date'))
    return data

def userlogs_data(request):
    user = user_models.UserProfile.objects.get(username=request.GET.get('username'))
    loglist = models.Jump_logs.objects.filter(username=user)
    return loglist