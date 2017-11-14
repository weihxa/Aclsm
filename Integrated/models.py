#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.db import models
from Integrated.user_models import UserProfile
# Create your models here.

class Authoritys(models.Model):
    event_type_choices = (
        ('1', u'Empowerment'),
        ('2', u'NoEmpowerment'),
    )
    user_name = models.ForeignKey(UserProfile,verbose_name=u'用户名')
    mark = models.CharField(u'权限', choices=event_type_choices, max_length=64, blank=True, null=True)
    Auth_name = models.CharField(u'app', max_length=64,blank=True)
    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = "权限表"


class Weekly(models.Model):
    user_name = models.ForeignKey(UserProfile, verbose_name=u'用户名')
    weeklys = models.CharField(u'重点工作事项',  max_length=128, blank=True, null=True)
    workplan = models.CharField(u'工作计划',  max_length=128, blank=True, null=True)
    completion = models.CharField(u'本周计划完成情况',  max_length=128, blank=True, null=True)
    coordination = models.CharField(u'工作难点及所需协调的资源',  max_length=128, blank=True, null=True)
    nextweek = models.CharField(u'下周工作计划',  max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)


    class Meta:
        verbose_name = '工作计划'
        verbose_name_plural = "工作计划"