#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

from django.db import models
# Create your models here.


class device_config(models.Model):

    description = models.CharField(u'描述', max_length=64,blank=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    password = models.CharField(u'密码',max_length=128,blank=True)
    group = models.ManyToManyField('group_config', verbose_name=u'属组',blank=True)
    memo = models.CharField(u'配置',max_length=64, null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = "主机信息"
    def __unicode__(self):
        return self.ipaddress

class group_config(models.Model):

    group_name = models.CharField(u'组名', max_length=64,blank=True)
    tomcat_puth = models.CharField(u'推送tomcat路径',max_length=128,null=True,blank=True)
    nginx_puth = models.CharField(u'推送nginx路径',max_length=128,null=True,blank=True)
    description = models.TextField(u'备注', max_length=64,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '组信息'
        verbose_name_plural = "组信息"
    def __unicode__(self):
        return self.group_name


class group_device(models.Model):

    group_name = models.ForeignKey(group_config,verbose_name=u'组名')
    device_name = models.ForeignKey(device_config,verbose_name=u'机器名')
    description = models.TextField(u'备注', max_length=64,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '组和成员对照表'
        verbose_name_plural = "组和成员对照表"
    def __unicode__(self):
        return self.group_name


class configuration_file(models.Model):
    event_type_choices = (
        ('1', u'nginx'),
        ('2', u'tomcat'),
        ('3', u'nginxinstall'),
        ('4', u'tomcatinstall'),
    )
    file_name = models.CharField(u'显示名', max_length=32,blank=True)
    file_content = models.TextField(u'配置文件', max_length=256,blank=True,null=True)
    mark = models.CharField(u'标识',choices=event_type_choices,max_length=64,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '配置文件表'
        verbose_name_plural = "配置文件表"
    def __unicode__(self):
        return self.file_name


class Package(models.Model):
    rpm_name = models.CharField(u'软件包名', max_length=64,blank=True)
    headImg = models.FileField(upload_to = './upload/')
    description = models.TextField(u'备注', max_length=64, blank=True)
    class Meta:
        verbose_name = '软件包表'
        verbose_name_plural = "软件包表"

    def __unicode__(self):
        return self.rpm_name

class task(models.Model):
    event_type_choices = (
        ('1', u'成功'),
        ('2', u'失败'),
        ('3', u'进行中'),
    )
    task_name = models.CharField(u'任务名', max_length=64,blank=True,null=True)
    task_Operated = models.CharField(u'被操作IP或组名',max_length=1024,blank=True,null=True)
    config_name = models.CharField(u'被推送配置文件名',max_length=128,blank=True,null=True)
    task_log = models.TextField(u'操作日志',max_length=2048,null=True)
    task_result = models.CharField(u'操作结果',choices=event_type_choices,max_length=64,blank=True,null=True)
    class Meta:
        verbose_name = '操作记录表'
        verbose_name_plural = "操作记录表"

    def __unicode__(self):
        return self.task_name