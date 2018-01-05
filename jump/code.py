#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
import models
import cryption
from SCMS import models as scms_models
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
    # print group_data[0].dev_list.split(',')[0]
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