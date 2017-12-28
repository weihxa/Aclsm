#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.db import models
from django.contrib import admin


class Jump_user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(u'账户名称',max_length=30,blank=True, null=True)
    permiss = models.TextField(u'sudo权限')
    create_date = models.DateTimeField(editable=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = '远程账户表'
        verbose_name_plural = "远程账户表"
    def __unicode__(self):
        return self.username

admin.site.register(Jump_user)