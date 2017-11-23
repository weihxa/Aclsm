#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,render_to_response
from asset import models,utils,asset_handle
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from asset import cabinet_views
import chart_output
from Integrated.plugins.Decorators import Perm_verification
import  core,ansible_caiji
import tasks

# @login_required
# def index(request):
#     return render(request,'index.html')

@login_required
@Perm_verification(perm='cmdb')
def index(request):
    data = chart_output.engine_room()
    status = chart_output.Machine_status()
    Business = chart_output.Business_Line()

    #return render_to_response('index.html',{'data':data,'status':status,'Business':Business})
    return render(request,'assets/index.html',{'data':data,'status':status,'Business':Business})




def new_assets_approval(request):
    tasks.update_cmdb.delay()
    return HttpResponse('ok')

@login_required
@Perm_verification(perm='cmdb')
def asset_list(request):

    return render(request,'assets/assets.html')

@login_required
@Perm_verification(perm='cmdb')
def get_asset_list(request):

    asset_dic = asset_handle.fetch_asset_list()
    # print(asset_dic)

    return HttpResponse(json.dumps(asset_dic,default=utils.json_date_handler))

@login_required
@Perm_verification(perm='cmdb')
def asset_category(request):
    category_type = request.GET.get("category_type")
    if not category_type:category_type='server'
    if request.is_ajax():
        categories = asset_handle.AssetCategroy(request)
        data = categories.serialize_data()
        return HttpResponse(data)
    else:
        return  render(request,'assets/asset_category.html',{'':category_type})


@login_required
@Perm_verification(perm='cmdb')
def asset_Cabinet(request):
    error = None
    data = cabinet_views.Cabinet_data()
    if len(data) == 0:
        error ='暂无机柜'
    return render(request,'assets/cabinet.html',{"asset_obj":data,'error':error})


@login_required
@Perm_verification(perm='cmdb')
def asset_Knifebox_logs(request,asset_id):
    if request.method == "GET":
        log_list = asset_handle.fetch_asset_Knifebox_logs(asset_id)
        return HttpResponse(json.dumps(log_list,default=utils.json_datetime_handler))

@login_required
@Perm_verification(perm='cmdb')
def asset_detail(request,asset_id):
    if request.method == "GET":
        try:
            asset_obj = models.Asset.objects.get(id=asset_id)

        except ObjectDoesNotExist as e:
            return render(request,'assets/asset_detail.html',{'error':e})
        return render(request,'assets/asset_detail.html',{"asset_obj":asset_obj})