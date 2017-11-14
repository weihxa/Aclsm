#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task
import datetime
from loghunter import models
from loghunter.plugins import paramiko_cmd,get_hostname
from xbmanIntegrated import settings
import re


@task
def get_database():
    print '开始更新磁盘空间信息'
    begin = datetime.datetime.now()
    models.disk.objects.all().delete()
    try:
        for i in paramiko_cmd.modify_paramiko(settings.ipaddr).killtomcat(cmd="salt '*' disk.percent / --out=txt"):
            name = i.split(':')[0].strip('\n') + ':' + get_hostname.get_ip(i.split(':')[0].strip('\n'))[1]
            models.disk.objects.create(name=name, mark=i.split(':')[1].strip('\n').strip())
    except Exception, e:
        print 'salt主机连接异常！'
    print '磁盘空间信息更新完成'
    end = datetime.datetime.now()
    print '处理时间:%s'%str(end-begin)
    return True

@task
def get_soft():
    print '开始更新软件版本信息'
    begin = datetime.datetime.now()
    models.softver.objects.all().delete()
    models.tomcatver.objects.all().delete()
    try:
        for i in  paramiko_cmd.modify_paramiko(settings.ipaddr).killtomcat(cmd="salt '*' grains.item 'kernelrelease' --out=txt"):
            name = i.split(':')[0].strip('\n') + ':' + get_hostname.get_ip(i.split(':')[0].strip('\n'))[1]
            try:
                kernel =  i.split(':')[2].strip('\n').strip('}')
            except IndexError ,e:
                kernel = '未获取'
            models.softver.objects.create(name=name,Kernel=kernel)
        for i in paramiko_cmd.modify_paramiko(settings.ipaddr).killtomcat(
                cmd="salt '*' state.sls getversion.getnginx --out=txt"):
            name = i.split(':')[0].strip('\n') + ':' + get_hostname.get_ip(i.split(':')[0].strip('\n'))[1]
            try:
                nginx_version = re.findall('nginx/\d+\.\d+\.\d+', i)[0]
                openssl_version = re.findall('openssl-\d+\.\d+\.\d+\w+', i)[0]
                nginx = nginx_version+','+openssl_version
            except IndexError ,e:
                nginx = 'nginx未安装'
            models.softver.objects.filter(name=name).update(nginx=nginx)
        for i in paramiko_cmd.modify_paramiko(settings.ipaddr).killtomcat(
                cmd="salt '*' state.sls getversion.gettomcat --out=txt"):
            name = i.split(':')[0].strip('\n') + ':' + get_hostname.get_ip(i.split(':')[0].strip('\n'))[1]
            tomcat_version = re.findall('[\\\]?\w+.\w+.\w+:Server number:\s+\d+\.\d+\.\d+\.\d+', i)
            if tomcat_version:
                for i in tomcat_version:
                    print i.strip("\\n")
                    models.tomcatver.objects.create(name=name,tomcat=i.strip("\\n"))
            else:
                models.tomcatver.objects.create(name=name, tomcat='tomcat未安装')
    except Exception, e:
        print 'salt主机连接异常！'
    print '软件版本信息更新完成'
    end = datetime.datetime.now()
    print '处理时间:%s' % str(end - begin)
