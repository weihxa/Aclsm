#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.core.exceptions import PermissionDenied
from functools import wraps
from Integrated import models

def get_auth(user):
    lists = []
    r_value = {'cmdb':False,'jenkins':False,'ansible':False,'logs':False,'jump':False}
    if user.is_admin:
        return {'cmdb':True,'jenkins':True,'ansible':True,'logs':True,'jump':True}
    for item in  models.Authoritys.objects.filter(user_name=user).values('Auth_name'):
        lists.append(item['Auth_name'])
    if 'cmdb' in lists:
        r_value['cmdb'] = True
    if 'jenkins' in lists:
        r_value['jenkins'] = True
    if 'ansible' in lists:
        r_value['ansible'] = True
    if 'logs' in lists:
        r_value['logs'] = True
    if 'jump' in lists:
        r_value['jump'] = True
    return r_value

def get_perm(user,perm):
    try:
        if models.Authoritys.objects.filter(user_name=user,Auth_name=perm).count() != 0:
            return True
    except AttributeError,e:
        return False


def admin_Auth(func):
    """
    验证是否是admin用户
    """
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
            if request.user.is_admin:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
    return returned_wrapper

def system_Auth(func):
    """
    验证用户访问系统权限
    """

    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        authoritys = get_auth(request.user)
        return func(request,authoritys=authoritys, *args, **kwargs)
    return returned_wrapper

def Perm_verification(perm):
    """
        验证针对系统权限验证
    """
    def entrance(func):
        @wraps(func)
        def inner(request,*args, **kvargs):
            if request.user.is_admin:
                return func(request, *args, **kvargs)
            if get_perm(user=request.user,perm=perm):
                return func(request,*args, **kvargs)
            else:
                raise PermissionDenied
        return inner
    return entrance