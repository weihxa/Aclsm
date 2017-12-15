#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task
import datetime
from SCMS import ansible_api
from asset import ansible_collection
from asset import core,models



@task
def update_cmdb():
    print '开始更新cmdb'
    begin = datetime.datetime.now()
    try:
        data = ansible_api.MyRunner().cmdrun(module_name='setup',pattern='*')['contacted']
        for k in data:
            datas = ansible_collection.collect(data[k])
            try:
                ass_handler = core.Asset(data=datas)
                ass_handler.data_inject()
            except Exception,e:
                print 'ERROR',e
    except Exception, e:
        print 'ERROR！',e
    print 'cmdb更新完成'
    end = datetime.datetime.now()
    models.Notice.objects.create(name=u'cmdb更/刷新成功',status=1)
    print '处理时间:%s'%str(end-begin)
    return True
