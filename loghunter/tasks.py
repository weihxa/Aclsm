#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task
import datetime
from loghunter import models
from SCMS import ansible_api


@task
def get_database():
    print '开始更新磁盘空间信息'
    begin = datetime.datetime.now()
    models.disk.objects.all().delete()
    data = ansible_api.MyRunner().cmdrun(module_name='setup', pattern='*')['contacted']
    try:
        for k in data:
            for i in data[k]['ansible_facts']['ansible_mounts']:
                if i['mount'] == '/':
                    mark = str(int(float(i['size_total']-i['size_available'])/float(i['size_available'])*100))+'%'
                    models.disk.objects.create(name=k, mark=mark)
    except Exception, e:
        print '磁盘空间更新失败，%s'%e
    print '磁盘空间信息更新完成'
    end = datetime.datetime.now()
    print '处理时间:%s'%str(end-begin)
    return True
