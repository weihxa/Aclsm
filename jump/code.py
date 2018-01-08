#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
import models
import cryption
from SCMS import models as scms_models
from Integrated import user_models
from Integrated import models as integr_models


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