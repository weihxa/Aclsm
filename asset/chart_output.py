#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from asset import models

def engine_room():
    data = {'room':[],'sum':[],'online':[],'shdown':[],'down':[],'maintain':[]}
    c_room_list = models.IDC.objects.all()
    for i in c_room_list:
        obj = models.Asset.objects.filter(idc__name__exact=i).filter(asset_type='server').count()
        if obj == 0:
            continue
        else:
            data['room'].append(i)
            data['sum'].append(obj)
            obj = models.Asset.objects.filter(idc__name__exact=i).filter(asset_type='server').filter(status='start').count()
            data['online'].append(obj)
            obj = models.Asset.objects.filter(idc__name__exact=i).filter(asset_type='server').filter(status='Disable').count()
            data['shdown'].append(obj)
            obj = models.Asset.objects.filter(idc__name__exact=i).filter(asset_type='server').filter(status='Disable_down').count()
            data['down'].append(obj)
            obj = models.Asset.objects.filter(idc__name__exact=i).filter(asset_type='server').filter(status='maintain').count()
            data['maintain'].append(obj)
    else:
        obj = models.Asset.objects.filter(idc=None).count()
        if obj != 0:
            data['room'].append('其他')
            data['sum'].append(obj)
            obj = models.Asset.objects.filter(idc=None).filter(asset_type='server').filter(status='start').count()
            data['online'].append(obj)
            obj = models.Asset.objects.filter(idc=None).filter(asset_type='server').filter(status='Disable').count()
            data['shdown'].append(obj)
            obj = models.Asset.objects.filter(idc=None).filter(asset_type='server').filter(status='Disable_down').count()
            data['down'].append(obj)
            obj = models.Asset.objects.filter(idc=None).filter(asset_type='server').filter(status='maintain').count()
            data['maintain'].append(obj)
    return data

def Machine_status():
    data = { 'online': [], 'shdown': [], 'down': [], 'maintain': []}
    obj = models.Asset.objects.filter(status='start').filter(asset_type='server').count()
    data['online']=obj
    obj = models.Asset.objects.filter(status='Disable').filter(asset_type='server').count()
    data['shdown']=obj
    obj = models.Asset.objects.filter(status='Disable_down').filter(asset_type='server').count()
    data['down']=obj
    obj = models.Asset.objects.filter(status='maintain').filter(asset_type='server').count()
    data['maintain']=obj
    return data

def Business_Line():
    data = {}
    Business_list = models.BusinessUnit.objects.all()
    for i in Business_list:
        obj = models.Asset.objects.filter(business_unit__name__exact=i).filter(asset_type='server').count()
        if obj == 0:
            continue
        else:
            data[i] = obj
    else:
        obj = models.Asset.objects.filter(business_unit=None).filter(asset_type='server').count()
        if obj != 0:
            data['未定义产品线'] = obj
    return data