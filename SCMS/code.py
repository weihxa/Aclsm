#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import froms
import os
import tasks
import ansible_api


project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def index(request):
    containerd ={}
    mainnn = {}
    business = {}
    containerd['dev'] = models.device_config.objects.all().count()
    containerd['group'] = models.group_config.objects.all().count()
    containerd['file'] = models.configuration_file.objects.all().count()
    containerd['task'] = models.task.objects.all().count()
    mainnn['success'] = models.task.objects.filter(task_result='1').count()
    mainnn['fail'] = models.task.objects.filter(task_result='2').count()
    mainnn['proces'] = models.task.objects.filter(task_result='3').count()
    business['nginx'] = models.configuration_file.objects.filter(mark='1').count()
    business['tomcat'] = models.configuration_file.objects.filter(mark='2').count()
    business['ninstall'] = models.configuration_file.objects.filter(mark='3').count()
    business['tinstall'] = models.configuration_file.objects.filter(mark='4').count()
    return containerd,mainnn,business
def pcmanage_post(request):
    try:
        if  models.device_config.objects.filter(ipaddress=request.POST.get('ipAddress')):
            return (False,'IP地址重复！请检查！')
        else:
            mark = ansible_api.MyRunner().deploy_key(server=request.POST.get('ipAddress'),
                                              username='root',
                                              password=request.POST.get('password')
            )
            if mark[0]:
                dev = models.device_config(description=request.POST.get('description'),
                                                           ipaddress=request.POST.get('ipAddress'),
                                                           memo=request.POST.get('Configuration'),
                                        )
                dev.save()
                for i in  request.POST.getlist('group'):
                    grou = models.group_config.objects.get(group_name=i)
                    dev.group.add(grou)
                    dev.save()
                return (True,'添加成功')
            else:
                return mark
    except Exception,e:
        print e

def pcmamage_get(request):
    group_list = models.group_config.objects.all()
    contact_list = models.device_config.objects.all().order_by('id')
    paginator = Paginator(contact_list, 20)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts,group_list

def del_device(request):
    models.device_config.objects.get(id=request.POST.get('modify')).delete()
    return True

def group_post(request):
    if  models.group_config.objects.filter(group_name=request.POST.get('groupname')):
        return False
    else:
        print request.POST.get('tomcat')
        dev,message = models.group_config.objects.get_or_create(group_name=request.POST.get('groupname'),
                                                                tomcat_puth=request.POST.get('tomcat'),
                                                                nginx_puth=request.POST.get('nginx'),
                                                                description=request.POST.get('description'))
        return message

def group_get(request):
    group_list = models.group_config.objects.all().order_by('id')
    paginator = Paginator(group_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

def del_group(request):
    models.group_config.objects.get(id=request.POST.get('modify')).delete()
    return True

def edit_group(request):
    models.group_config.objects.filter(id=request.POST.get('id')).update(
        nginx_puth=request.POST.get('nginx2'), tomcat_puth=request.POST.get('tomcat2'),
        description=request.POST.get('description2'))
    return True

def config_post(request):
    if  models.configuration_file.objects.filter(mark=request.POST.get('description')).filter(
            file_name=request.POST.get('confname')):
        return False
    else:
        dev,message = models.configuration_file.objects.get_or_create(file_name=request.POST.get('confname'),
                                                                      file_content=request.POST.get('neweditor'),
                                                                      mark=request.POST.get('description'))
        return message

def config_edit(request):
    models.configuration_file.objects.filter(id=request.POST.get('confid')).update(
        file_name=request.POST.get('confnams'), file_content=request.POST.get('editor'))
    return True

def config_get(request):
    conf_list = models.configuration_file.objects.filter(mark='1').order_by('id')
    profile_list = models.configuration_file.objects.filter(mark='2').order_by('id')
    nginx_list = models.configuration_file.objects.filter(mark='3').order_by('id')
    tomcat_list = models.configuration_file.objects.filter(mark='4').order_by('id')
    return conf_list,profile_list,nginx_list,tomcat_list

def del_config(request):
    models.configuration_file.objects.get(id=request.POST.get('modify')).delete()
    return True

def pageadd(request):
    uf = froms.headImg(request.POST, request.FILES)
    if uf.is_valid():
        headImg = uf.cleaned_data['headImg']
        # 写入数据库
        user = models.Package()
        user.rpm_name = headImg
        user.headImg = headImg
        user.description = request.POST.get("description")
        user.save()
        return True
    else:
        return False
def pageget(request):
    page_list = models.Package.objects.all()
    return page_list

def del_page(request):
    # project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    filename = models.Package.objects.filter(id=request.POST.get('modify')).values('rpm_name')
    filenamde = project_dir+'/upload/'+ str(filename[0]['rpm_name'])
    if os.path.exists(filenamde):
        os.remove(filenamde)
        models.Package.objects.get(id=request.POST.get('modify')).delete()
        return True
    else:
        return False

def code_generate(request):
    #生成ansible主机配置文件
    os.system('mkdir %s'%os.path.join(project_dir,'temp'))
    with open(project_dir+'/temp/'+'hosts','w') as f:
        for i in models.device_config.objects.all().order_by('id'):
            f.write(i.ipaddress+'\n')
        for item in models.group_config.objects.all().order_by('id'):
            f.write('['+item.group_name.encode('utf-8')+']'+'\n')
            for i in models.device_config.objects.filter(group__group_name=item.group_name):
                f.write(i.ipaddress+'\n')
    return True


def tasks_get(request):
    contact_list = models.task.objects.all().order_by('-id')
    paginator = Paginator(contact_list, 20)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

def nginxpush_get(request):
    contacts = models.device_config.objects.all().order_by('ipaddress')
    config = models.configuration_file.objects.filter(mark='1').order_by('id')
    group = models.group_config.objects.all().order_by('id')
    return contacts,config,group

def nginxpush_post(request):
    if  request.POST.get('mark') == '1':
        tasks.nginxdev_push.delay(file=request.POST.get('file'),pclist=request.POST.getlist('pclist'),puthdir=request.POST.get('puthdir'))
    elif request.POST.get('mark') == '2':
        tasks.nginxgroup_push.delay(group=request.POST.get('group'),file=request.POST.get('file'),)
    return True

def tomcatpush_get(request):
    contacts = models.device_config.objects.all().order_by('ipaddress')
    config = models.configuration_file.objects.filter(mark='2').order_by('id')
    group = models.group_config.objects.all().order_by('id')
    return contacts,config,group

def tomcatpush_post(request):
    if  request.POST.get('mark') == '1':
        tasks.tomcatdev_push.delay(file=request.POST.get('file'),pclist=request.POST.getlist('pclist'),puthdir=request.POST.get('puthdir'))
    elif request.POST.get('mark') == '2':
        tasks.tomcatgroup_push.delay(group=request.POST.get('group'),file=request.POST.get('file'))
    return True

def ninstall_get(request):
    contacts = models.device_config.objects.all().order_by('ipaddress')
    config = models.configuration_file.objects.filter(mark='3').order_by('id')
    group = models.group_config.objects.all().order_by('id')
    return contacts,config,group

def ninstall_post(request):
    if  request.POST.get('mark') == '1':
        tasks.ninstall_push.delay(request.POST.getlist('pclist'),request.POST.get('file'))
    elif request.POST.get('mark') == '2':
        tasks.ninstallgroup_push.delay(request.POST.get('group'),request.POST.get('file'))
    return True


def tinstall_get(request):
    contacts = models.device_config.objects.all().order_by('ipaddress')
    config = models.configuration_file.objects.filter(mark='4').order_by('id')
    group = models.group_config.objects.all().order_by('id')
    return contacts,config,group

def tinstall_post(request):
    if  request.POST.get('mark') == '1':
        tasks.tinstall_push.delay(request.POST.getlist('pclist'),request.POST.get('file'))
    elif request.POST.get('mark') == '2':
        tasks.tinstallgroup_push.delay(request.POST.get('group'),request.POST.get('file'))
    return True

def cmdrun(request):
    log = []
    if 'shutdown' in request.POST.get('cmd') or 'init 0' in request.POST.get('cmd') or 'init 6' in request.POST.get('cmd') or 'reboot' in request.POST.get('cmd') or len(request.POST.get('cmd').strip()) == 0:
        data = {'status': 1, 'msg': '请求失败', 'data': '执行命令中存在shutdown,init 0,init 6,reboot等敏感命令或执行命令未填写，不允许执行！！'}
        return data
    if  request.POST.get('mark') == '1':
        iplist = []
        for i in request.POST.getlist('pclist'):
            item = models.device_config.objects.get(id=i)
            iplist.append(item.ipaddress)
            date = ansible_api.MyRunner().cmdrun(pattern=item.ipaddress,module_args=request.POST.get('cmd'))['contacted']
            log.append(item.ipaddress+':')
            log.append(date[item.ipaddress]['stdout'] + '\n')
        data = {'status': 0, 'msg': '请求成功', 'data': '\n'.join(log)}
        return data
    elif request.POST.get('mark') == '2':
        for i in models.device_config.objects.filter(group=request.POST.get('group')):
            date = ansible_api.MyRunner().cmdrun(pattern=i.ipaddress,
                                                                     module_args=request.POST.get('gcmd'))['contacted']
            log.append(i.ipaddress + ':')
            log.append(date[i.ipaddress]['stdout'] + '\n')
        data = {'status': 0, 'msg': '请求成功', 'data': '\n'.join(log)}
        return data