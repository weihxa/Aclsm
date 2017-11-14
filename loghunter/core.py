#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
import json
import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Integrated import user_models
import urllib2
from xbmanIntegrated import settings
from django.db.models import Q

def index():
    containerd = {}
    containerd['early'] = models.Early_warn.objects.all().values('ipaddress').distinct().count()
    containerd['group'] = models.disk.objects.all().values('name').distinct().count()
    return containerd

def report_url(msg):
    new_url = 'http://localhost:8080/sms/inner?mobile=%s&content=%s'%(settings.p_number,msg)
    try:
        req = urllib2.Request(url=new_url,)
        res_data = urllib2.urlopen(req, timeout=30)
        callback = res_data.read()
        print  callback
        return '入库成功，短信已发送'
    except urllib2.URLError, e:
        print('url无法访问，短信发送失败！')
        return '入库成功，但短信发送失败'

def report(request):
    data = json.loads(request.POST.get('data'))
    if len(data['ipaddr']) == 0:
        return '汇报数据中IP地址为空，请检查配置！'
    dev, message =models.Early_warn.objects.get_or_create(ipaddress=data['ipaddr'],
                                                    mark=data['mark'],
                                                    report_msm=json.dumps(data['data']))
    if message:
        msg = "Active warning report：mark[%s],ip:[%s],click this link to view report：[%s]" % (
        str(data['mark']), str(data['ipaddr']), 'http://10.66.48.7:8001/detailreport/?ip=' + str(data['ipaddr']))
        # print msg
        # report_url(msg=msg)
        if settings.Notice:
            return report_url(msg=msg)
        else:
            return '入库成功，服务端未设置短信通知'
    else:
        return '重复上报！'

def get_report():
    data_list = []
    for i in models.Early_warn.objects.all().values('ipaddress').distinct().order_by('-ipaddress'):
        data = {"ipaddress": "", "num": "", "datatime": "", "mark": ""}
        data['ipaddress'] = i['ipaddress']
        obj_data = models.Early_warn.objects.filter(ipaddress=i['ipaddress']).order_by('-report_date')
        data['datatime'] = str(obj_data.values('report_date')[0]['report_date'])
        data['num'] = obj_data.count()
        data['mark'] = obj_data.values('mark')[0]['mark']
        data_list.append(data)
    return data_list

def get_deatil(ipaddress):
    data_list = []
    for i in models.Early_warn.objects.filter(ipaddress=ipaddress).order_by('-report_date').all():
        data = {"datatime": "", "mark": "", "id": ""}
        data['datatime'] = str(i.report_date)
        data['mark'] = i.mark
        data['id'] = i.id
        data_list.append(data)
    return data_list

def get_deatil_logs(id):
    data = models.Early_warn.objects.filter(id=id).values('report_msm')[0]['report_msm']
    return ''.join(json.loads(data))

def get_disk():
    normal = []
    unusual = []
    for i in models.disk.objects.all():
        data = {'id': '', 'name': '', 'mark': ''}
        if 'did not' in i.mark:
            data['id'] = i.id
            data['name'] = i.name
            data['mark'] = i.mark
            unusual.append(data)
        elif int(i.mark.strip('%')) >= 60:
            data['id'] = i.id
            data['name'] = i.name
            data['mark'] = i.mark
            unusual.append(data)
        elif int(i.mark.strip('%')) < 60:
            data['id'] = i.id
            data['name'] = i.name
            data['mark'] = i.mark
            normal.append(data)
    return normal,unusual

def get_softversion():
    data_list = []
    for i in models.softver.objects.all().order_by('-name'):
        data = {"name": "", "Kernel": "", "nginx": ""}
        data['name'] = i.name
        data['Kernel'] = i.Kernel.strip().strip("'")
        data['nginx'] = i.nginx
        data_list.append(data)
    return data_list