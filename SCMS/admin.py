#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.contrib import admin
from SCMS import models
from django.contrib.auth.models import Group
# Register your models here.


class device_config(admin.ModelAdmin):
    list_display = ('description','ipaddress')
    search_fields = ('ipaddress',)

class group_config(admin.ModelAdmin):
    list_display = ('group_name',)
    search_fields = ('group_name',)

class group_device(admin.ModelAdmin):
    list_display = ('group_name',)
    search_fields = ('group_name',)

class configuration_file(admin.ModelAdmin):
    list_display = ('file_name',)
    search_fields = ('file_name',)

class Package(admin.ModelAdmin):
    list_display = ('rpm_name',)
    search_fields = ('rpm_name',)
class Task(admin.ModelAdmin):

    list_display = ('task_name',)
    search_fields = ('task_name',)



admin.site.register(models.device_config,device_config)
admin.site.register(models.group_config,group_config)
admin.site.register(models.group_device,group_device)
admin.site.register(models.configuration_file,configuration_file)
admin.site.register(models.Package,Package)
admin.site.register(models.task,Task)
admin.site.register(models.Playbook)
# admin.site.unregister(Group)