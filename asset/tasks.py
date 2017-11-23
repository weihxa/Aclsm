#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task
import datetime,json
from SCMS import ansible_api
from asset import ansible_caiji
from asset import core



@task
def update_cmdb():
    print '开始更新cmdb'
    begin = datetime.datetime.now()
    try:
        data = ansible_api.MyRunner().cmdrun(module_name='setup',pattern='*')['contacted']
        for k,v in data.items():
            data = ansible_caiji.collect(v)
            ass_handler = core.Asset(data=data)
            ass_handler.data_inject()
    except Exception, e:
        print 'salt主机连接异常！'
    print '开始更新cmdb更新完成'
    end = datetime.datetime.now()
    print '处理时间:%s'%str(end-begin)
    return True
