#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

from celery import task
from confile_process import process
import models
# import ansible_api

@task
def nginxdev_push(file,pclist,puthdir):
    iplist = []
    log = []
    confname, path = process().nginx_conf(id=file)
    for i in pclist:
        item = models.device_config.objects.get(id=i)
        iplist.append(item.ipaddress)
    obj = models.task(task_name='nginx推送',config_name=confname, task_Operated=','.join(iplist),task_result=3)
    obj.save()
    obj_id = obj.id

    if len(puthdir.strip()) == 0:
        module_args = 'src=%s dest=/tmp/nginx.conf'%path
    else:
        module_args = 'src=%s dest=/%s/nginx.conf' %(path,puthdir.strip().strip('/'))

    date = ansible_api.MyRunner().cmdrun(pattern=','.join(iplist),module_name='copy',
                                                          module_args=module_args)['contacted']

    task_result = 1
    for i in iplist:
        try:
            log.append(i + ':')
            log.append(str(date[i]['changed']) + '\n')
        except Exception,e:
            log.append(str(date[i]['msg']) + '\n')
            task_result = 2
            continue
    models.task.objects.filter(id=obj_id).update(task_result=task_result,task_log='\n'.join(log))


@task
def nginxgroup_push(group,file):
    log = []
    item = models.group_config.objects.get(id=group)
    confname,path = process().nginx_conf(id=file)
    obj = models.task(task_name='nginx组推送',config_name=confname, task_Operated=item.group_name,task_result=3)
    obj.save()
    obj_id = obj.id
    if len(item.nginx_puth.strip()) == 0:
        module_args = 'src=%s dest=/tmp/nginx.conf' % path
    else:
        module_args = 'src=%s dest=/%s/nginx.conf' % (path, item.nginx_puth.strip().strip('/'))
    try:
        for i in models.device_config.objects.filter(group=group):
            date = ansible_api.MyRunner().cmdrun(pattern=i.ipaddress,module_name='copy',
                                                                       module_args=module_args)['contacted']
            log.append(i.ipaddress + ':')
            log.append(str(date[i.ipaddress]['changed']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1,task_log='\n'.join(log))
    except Exception,e:
        models.task.objects.filter(id=obj_id).update(task_result=2,
                                                     task_log='被控制机没有安装libselinux-python，或网络不可达！')

@task
def tomcatdev_push(file,pclist,puthdir):
    ipdict = {}
    log = []
    confname,path = process().tomcat_conf(id=file)
    for i in pclist:
        item = models.device_config.objects.get(id=i)
        ipdict[item.ipaddress] = item.password
    obj = models.task(task_name='tomcat推送', config_name=confname, task_Operated=','.join(ipdict.keys()), task_result=3)
    obj.save()
    obj_id = obj.id
    if len(puthdir.strip()) == 0:
        module_args = 'src=%s dest=/tmp/server.xml' % path
    else:
        module_args = 'src=%s dest=/%s/server.xml' % (path,puthdir.strip().strip('/'))
    try:
        for k, y in ipdict.items():
            date = ansible_api.MyRunner().cmdrun(pattern=k, module_name='copy',
                                                              module_args=module_args)[
                'contacted']
            log.append(k + ':')
            log.append(str(date[k]['changed']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1, task_log='\n'.join(log))
    except Exception,e:
        models.task.objects.filter(id=obj_id).update(task_result=2,
                                                     task_log='被控制机没有安装libselinux-python，或网络不可达！')

@task
def tomcatgroup_push(group,file):
    log = []
    item = models.group_config.objects.get(id=group)
    confname, path = process().tomcat_conf(id=file)
    obj = models.task(task_name='tomcat组推送', config_name=confname, task_Operated=item.group_name, task_result=3)
    obj.save()
    obj_id = obj.id
    if len(item.tomcat_puth.strip()) == 0:
        module_args = 'src=%s dest=/tmp/server.xml' % path
    else:
        module_args = 'src=%s dest=/%s/server.xml' % (path, item.tomcat_puth.strip().strip('/'))
    try:
        for i in models.device_config.objects.filter(group=group):
            date = ansible_api.MyRunner().cmdrun(pattern=i.ipaddress, module_name='copy',
                                                                       module_args=module_args)[
                'contacted']
            log.append(i.ipaddress + ':')
            log.append(str(date[i.ipaddress]['changed']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1, task_log='\n'.join(log))
    except Exception,e:
        models.task.objects.filter(id=obj_id).update(task_result=2,
                                                     task_log='被控制机没有安装libselinux-python，或网络不可达！')

@task
def ninstall_push(pclist,id):
    ipdict = {}
    log = []
    confname, path = process().nginxinstall_conf(id=id)
    for i in pclist:
        item = models.device_config.objects.get(id=i)
        ipdict[item.ipaddress] = item.password
    obj = models.task(task_name='nginx安装', config_name=confname, task_Operated=','.join(ipdict.keys()), task_result=3)
    obj.save()
    obj_id = obj.id
    try:
        for k, y in ipdict.items():
            date = ansible_api.MyRunner().PlayBook_execute(play=path,params='{"host": "%s"}'%k)
            log.append(k + ':')
            log.append(str(date[k]['failures']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1, task_log='\n'.join(log))
    except Exception, e:
        models.task.objects.filter(id=obj_id).update(task_result=2, task_log='被控制机没有安装libselinux-python，或网络不可达！')

@task
def ninstallgroup_push(group_id,id):
    log = []
    item = models.group_config.objects.get(id=group_id)
    confname, path = process().nginxinstall_conf(id=id)
    obj = models.task(task_name='nginx组安装', config_name=confname, task_Operated=item.group_name, task_result=3)
    obj.save()
    obj_id = obj.id
    try:
        for i in models.device_config.objects.filter(group=group_id):
            date = ansible_api.MyRunner().PlayBook_execute(play=path,params='{"host": "%s"}'%i.ipaddress)
            log.append(i.ipaddress + ':')
            log.append(str(date[i.ipaddress]['failures']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1, task_log='\n'.join(log))
    except Exception, e:
        models.task.objects.filter(id=obj_id).update(task_result=2, task_log='被控制机没有安装libselinux-python，或网络不可达！')

@task
def tinstall_push(pclist,id):
    ipdict = {}
    log = []
    confname, path = process().tomcatinstall_conf(id=id)
    for i in pclist:
        item = models.device_config.objects.get(id=i)
        ipdict[item.ipaddress] = item.password
    obj = models.task(task_name='tomcat安装', config_name=confname, task_Operated=','.join(ipdict.keys()), task_result=3)
    obj.save()
    obj_id = obj.id
    try:
        for k, y in ipdict.items():
            date = ansible_api.MyRunner().PlayBook_execute(play=path, params='{"host": "%s"}' % k)
            log.append(k + ':')
            log.append(str(date[k]['failures']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1, task_log='\n'.join(log))
    except Exception, e:
        models.task.objects.filter(id=obj_id).update(task_result=2, task_log='被控制机没有安装libselinux-python，或网络不可达！')

@task
def tinstallgroup_push(group_id,id):
    log = []
    item = models.group_config.objects.get(id=group_id)
    confname, path = process().tomcatinstall_conf(id=id)
    obj = models.task(task_name='tomcat组安装', config_name=confname, task_Operated=item.group_name, task_result=3)
    obj.save()
    obj_id = obj.id
    try:
        for i in models.device_config.objects.filter(group=group_id):
            date = ansible_api.MyRunner().PlayBook_execute(play=path,
                                                                                 params='{"host": "%s"}' % i.ipaddress)
            log.append(i.ipaddress + ':')
            log.append(str(date[i.ipaddress]['failures']) + '\n')
        models.task.objects.filter(id=obj_id).update(task_result=1, task_log='\n'.join(log))
    except Exception, e:
        models.task.objects.filter(id=obj_id).update(task_result=2, task_log='被控制机没有安装libselinux-python，或网络不可达！')