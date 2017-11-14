#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.contrib import admin
from Integrated import models
from user_admin import UserAdmin
from django.contrib.auth.models import Group
# Register your models here.
class device_config(admin.ModelAdmin):
    list_display = ('user_name','mark','Auth_name')
    search_fields = ('Auth_name',)
class Weekly_config(admin.ModelAdmin):
    list_display = ('user_name','weeklys')
    search_fields = ('user_name',)
admin.site.register(models.UserProfile,UserAdmin)
admin.site.register(models.Authoritys,device_config)
admin.site.register(models.Weekly,Weekly_config)
admin.site.unregister(Group)