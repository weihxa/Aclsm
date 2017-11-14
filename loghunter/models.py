#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.db import models
from django.contrib import admin

# Create your models here.
class Early_warn(models.Model):
    id = models.AutoField(primary_key=True)
    ipaddress = models.GenericIPAddressField(u'IP地址', blank=True, null=True)
    mark = models.CharField(u'故障标识',max_length=30)
    report_msm = models.TextField(u'汇报信息')
    report_date = models.DateTimeField(editable=True,blank=True,auto_now_add=True)

    class Meta:
        verbose_name = '异常抓取推送'
        verbose_name_plural = "异常抓取推送"
    def __unicode__(self):
        return self.ipaddress

class YourAdmin(admin.ModelAdmin):
    list_display = ('ipaddress','report_date')
    ordering = ('report_date',)
    search_fields = ('report_date',)
    list_filter = ('report_date',)
admin.site.register(Early_warn,YourAdmin)

class disk(models.Model):
    name = models.CharField(u'主机',max_length=256)
    mark = models.CharField(u'空间',max_length=80)
    create_date = models.DateTimeField(editable=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = '磁盘空间'
        verbose_name_plural = "磁盘空间"
    def __unicode__(self):
        return self.name

class diskadmin(admin.ModelAdmin):
    list_display = ('name','mark')
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(disk,diskadmin)


class softver(models.Model):
    name = models.CharField(u'主机',max_length=256)
    Kernel = models.CharField(u'内核',max_length=80)
    nginx = models.CharField(u'nginx',max_length=80)
    create_date = models.DateTimeField(editable=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = '软件版本'
        verbose_name_plural = "软件版本"
    def __unicode__(self):
        return self.name

class softveradmin(admin.ModelAdmin):
    list_display = ('name','Kernel')
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(softver,softveradmin)

class tomcatver(models.Model):
    name = models.CharField(u'主机',max_length=256)
    tomcat = models.CharField(u'版本',max_length=80)
    create_date = models.DateTimeField(editable=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = 'tomcat版本'
        verbose_name_plural = "tomcat版本"
    def __unicode__(self):
        return self.name

class tomcatveradmin(admin.ModelAdmin):
    list_display = ('name','tomcat')
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(tomcatver,tomcatveradmin)