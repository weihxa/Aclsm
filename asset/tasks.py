#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task
import datetime
from SCMS import ansible_api
from asset import ansible_caiji
from asset import core



@task
def update_cmdb():
    print '开始更新cmdb'
    begin = datetime.datetime.now()
    try:
        data = ansible_api.MyRunner().cmdrun(module_name='setup',pattern='*')['contacted']
        for k in data:
            datas = ansible_caiji.collect(data[k])
            try:
                ass_handler = core.Asset(data=datas)
                ass_handler.data_inject()
            except Exception,e:
                print 'ERROR',e
    except Exception, e:
        print 'ERROR！',e
    print 'cmdb更新完成'
    end = datetime.datetime.now()
    print '处理时间:%s'%str(end-begin)
    return True
