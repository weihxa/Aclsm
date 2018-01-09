#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task
import datetime
# from SCMS import ansible_api
from jump import models
import commands
from jump import cryption


def handle_password(password):
    pawd = commands.getoutput('openssl passwd -salt -1 "%s"' % cryption.decrypt(password))
    return pawd.strip()

def handle_sshkey(ip,username,password):
    mark = ansible_api.MyRunner().deploy_key(server=ip,
                                      username=username,
                                      password=cryption.decrypt(password)
                                      )
    return mark

@task
def push_prem(dev):
    print '[堡垒机]开始推送账号及权限'
    begin = datetime.datetime.now()
    if dev == 'all':
        data = models.Jump_group.objects.all()
        for item in data:
            user = models.Jump_user.objects.filter(username=item.user)
            try:
                module_args = 'name=%s password=%s' % (item.user, handle_password(user[0].password))
                ansible_api.MyRunner().cmdrun(pattern=item.dev_list,
                                              module_name='user',
                                              module_args=module_args)['contacted']
                ansible_api.MyRunner().cmdrun(pattern=item.dev_list,
                                              module_args="/bin/echo '%s' >>/etc/sudoers" % user[0].permiss)['contacted']
                for i in item.dev_list.split(','):
                    mark = handle_sshkey(str(i), str(item.user), str(user[0].password))
                    print '[sshkey] ' + str(i) + str(mark[1])
            except Exception, e:
                print '[堡垒机]ERROR！', e
        print '[堡垒机]账号及权限推送完成'
        end = datetime.datetime.now()
        models.Jump_Notice.objects.create(name=u'all,账号及权限推送完成', status=1)
        print '[堡垒机]处理时间:%s' % str(end - begin)
        return True
    else:
        data = models.Jump_group.objects.filter(id=dev)
        user = models.Jump_user.objects.filter(username=data[0].user)
        try:
            module_args = 'name=%s password=%s'%(data[0].user,handle_password(user[0].password))
            ansible_api.MyRunner().cmdrun(pattern=data[0].dev_list,
                                                 module_name='user',
                                                 module_args=module_args)['contacted']
            ansible_api.MyRunner().cmdrun(pattern=data[0].dev_list,
                                                 module_args="/bin/echo '%s' >>/etc/sudoers"%user[0].permiss)['contacted']
            for i in data[0].dev_list.split(','):
                mark = handle_sshkey(str(i),str(data[0].user),str(user[0].password))
                print '[sshkey] '+str(i)+str(mark[1])
        except Exception, e:
            print '[堡垒机]ERROR！',e
        print '[堡垒机]账号及权限推送完成'
        end = datetime.datetime.now()
        models.Jump_Notice.objects.create(name=u'组[%s],账号及权限推送完成'%data[0].groupname,status=1)
        print '[堡垒机]处理时间:%s'%str(end-begin)
        return True