#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
import models
import cryption
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