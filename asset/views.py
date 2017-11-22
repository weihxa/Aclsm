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

import  cores,ansible_caiji

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
    aaaa = '''
    {"127.0.0.1": {"invocation": {"module_name": "setup", "module_complex_args": {}, "module_args": ""}, "verbose_override": true, "changed": false, "ansible_facts": {"ansible_product_serial": "VMware-56 4d e0 c4 1a c1 ba 46-ed 84 a5 bc 4d 09 ad 42", "ansible_form_factor": "Other", "ansible_product_version": "None", "ansible_fips": false, "ansible_swaptotal_mb": 1983, "ansible_user_id": "root", "module_setup": true, "ansible_userspace_bits": "64", "ansible_distribution_version": "6.9", "ansible_domain": "", "ansible_virtualization_type": "VMware", "ansible_processor_cores": 1, "ansible_virtualization_role": "guest", "ansible_env": {"LC_CTYPE": "en_US.UTF-8", "LESSOPEN": "||/usr/bin/lesspipe.sh %s", "SELINUX_ROLE_REQUESTED": "", "SELINUX_USE_CURRENT_RANGE": "", "LOGNAME": "root", "USER": "root", "HOME": "/root", "PATH": "/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin", "_": "/usr/bin/python", "LANG": "en_US.UTF-8", "SHELL": "/bin/bash", "SHLVL": "2", "G_BROKEN_FILENAMES": "1", "SSH_CLIENT": "127.0.0.1 46726 22", "SELINUX_LEVEL_REQUESTED": "", "PWD": "/root", "MAIL": "/var/mail/root", "SSH_CONNECTION": "127.0.0.1 46726 127.0.0.1 22"}, "ansible_processor_vcpus": 1, "ansible_bios_version": "6.00", "ansible_processor": ["GenuineIntel", "Intel(R) Core(TM) i3-4030U CPU @ 1.90GHz"], "ansible_date_time": {"tz": "CST", "hour": "15", "time": "15:07:02", "tz_offset": "+0800", "month": "11", "epoch": "1511161622", "iso8601_micro": "2017-11-20T07:07:02.589666Z", "weekday": "Monday", "year": "2017", "date": "2017-11-20", "iso8601": "2017-11-20T07:07:02Z", "day": "20", "minute": "07", "second": "02"}, "ansible_lo": {"active": true, "promisc": false, "ipv4": {"netmask": "255.0.0.0", "network": "127.0.0.0", "address": "127.0.0.1"}, "ipv6": [{"scope": "host", "prefix": "128", "address": "::1"}], "device": "lo", "type": "loopback", "mtu": 65536}, "ansible_memtotal_mb": 848, "ansible_architecture": "x86_64", "ansible_default_ipv4": {"macaddress": "00:0c:29:09:ad:42", "network": "192.168.177.0", "mtu": 1500, "alias": "eth0", "netmask": "255.255.255.0", "address": "192.168.177.128", "interface": "eth0", "type": "ether", "gateway": "192.168.177.2"}, "ansible_swapfree_mb": 1983, "ansible_default_ipv6": {}, "ansible_distribution_release": "Final", "ansible_system_vendor": "VMware, Inc.", "ansible_os_family": "RedHat", "ansible_cmdline": {"LANG": "zh_CN.UTF-8", "rd_NO_LUKS": true, "KEYBOARDTYPE": "pc", "rd_NO_MD": true, "quiet": true, "rd_LVM_LV": "vg_master/lv_root", "rhgb": true, "KEYTABLE": "us", "ro": true, "root": "/dev/mapper/vg_master-lv_root", "rd_NO_DM": true}, "ansible_user_gid": 0, "ansible_selinux": false, "ansible_userspace_architecture": "x86_64", "ansible_product_uuid": "564DE0C4-1AC1-BA46-ED84-A5BC4D09AD42", "ansible_system": "Linux", "ansible_pkg_mgr": "yum", "ansible_memfree_mb": 109, "ansible_devices": {"sr0": {"scheduler_mode": "cfq", "rotational": "1", "vendor": "NECVMWar", "sectors": "2097151", "host": "IDE interface: Intel Corporation 82371AB/EB/MB PIIX4 IDE (rev 01)", "sectorsize": "512", "removable": "1", "support_discard": "0", "model": "VMware IDE CDR10", "size": "1024.00 MB", "holders": [], "partitions": {}}, "sda": {"scheduler_mode": "cfq", "rotational": "1", "vendor": "VMware,", "sectors": "41943040", "host": "SCSI storage controller: LSI Logic / Symbios Logic 53c1030 PCI-X Fusion-MPT Dual Ultra320 SCSI (rev 01)", "sectorsize": "512", "removable": "0", "support_discard": "0", "model": "VMware Virtual S", "size": "20.00 GB", "holders": [], "partitions": {"sda2": {"start": "1026048", "sectorsize": 512, "sectors": "40916992", "size": "19.51 GB"}, "sda1": {"start": "2048", "sectorsize": 512, "sectors": "1024000", "size": "500.00 MB"}}}}, "ansible_user_uid": 0, "ansible_memory_mb": {"real": {"total": 848, "free": 109, "used": 739}, "swap": {"cached": 0, "total": 1983, "used": 0, "free": 1983}, "nocache": {"used": 415, "free": 433}}, "ansible_distribution": "CentOS", "ansible_ssh_host_key_dsa_public": "AAAAB3NzaC1kc3MAAACBALZN+r72hAJgfdAf98ZygbdKgeefGuoFRJ6tFMwYms8FjFr1jdglW0OV0yWYcWAUnWWKeuUVJW4fMyflL6ksNFu4odZa0Z3jKQU2Qn8aWuIkItC5TItkCZ+7rAwAvCqBSOc8FG+8NYmJDDwfAIYnNvgQzUThSuFEkUEqNOiFJGgtAAAAFQDxoV6U7JBkaiXzUOsrQb6SFFtoWQAAAIEAruKRPZGmWYOwUkbU/ilYlE9+SUSUJ2ZRiOk/6Lo4TNnh7QX92mSII4FhiKXDY5/ZMV4T260rneaT/9BwwESZF72La+xt216XCAFBxgsYASLCqsGVq00/NBqhX2Kv6rkhJYCfOiOmeMg4Mod9bx3A9sMbd+CQfE/GpwoXjjWDhv0AAACAd0zAU6JNPFImS5JFhnnuESfh+euoSR1mt0dT+X9RIlsTxgci6hfs/AfHb+zJ5NSnv3ekNEfeU0SSM/GnASZEWDjTirqjWFxmEH5TSMIDLOnZZIRV55+WVl6acKwx1DYLIIKsJ2TP+IKVih72pgERTMVD7yf4hl8nCpIcaCp2Raw=", "ansible_user_dir": "/root", "ansible_processor_count": 1, "ansible_hostname": "master", "ansible_bios_date": "07/02/2015", "ansible_all_ipv6_addresses": ["fe80::20c:29ff:fe09:ad42"], "ansible_interfaces": ["lo", "eth0"], "ansible_machine_id": "fbd9609d805e719ed208c7d90000001f", "ansible_ssh_host_key_rsa_public": "AAAAB3NzaC1yc2EAAAABIwAAAQEAovE86Fis8ZR9AkrfvmWPX+Jb7AZbc82ZClvrzQ613Mhnyf4v7+TuR2vpF5qKoALZCh+A4E9YPBkm1WpVHnF40GTwParWeBdkzao4VgS8s2baeURCF5AoEKN9HMpLdasTMn3ix8H2jduCuTseCUG3mxDCcikWWP6F2gTzQWjmeO/w9EWChPATnHNtl6lYb9m4Zq1hXWvs5A+EXMoBNDI6TbGHMTeRM2ZEsXsNI+6E6VV7LPa/Z7PMcmJKUFQ9MKe+2d6+4jHGVtKKPKFYp2uwn0XSGUDOpjL4LGJnC49PjBdDsGtSocETStS0ACnqZ+ytJzDHfEk3+p0kcxO8XuQLqw==", "ansible_machine": "x86_64", "ansible_user_gecos": "root", "ansible_kernel": "2.6.32-696.el6.x86_64", "ansible_processor_threads_per_core": 1, "ansible_fqdn": "master", "ansible_mounts": [{"options": "rw", "uuid": "fb4d97f4-d955-4b33-ba1e-29e6e4de4907", "size_total": 18435350528, "device": "/dev/mapper/vg_master-lv_root", "mount": "/", "size_available": 14842048512, "fstype": "ext4"}, {"options": "rw", "uuid": "614f8464-566b-47c5-a412-f61a8d0de42c", "size_total": 499355648, "device": "/dev/sda1", "mount": "/boot", "size_available": 431568896, "fstype": "ext4"}], "ansible_eth0": {"macaddress": "00:0c:29:09:ad:42", "module": "e1000", "mtu": 1500, "active": true, "promisc": false, "ipv4": {"netmask": "255.255.255.0", "network": "192.168.177.0", "address": "192.168.177.128"}, "ipv6": [{"scope": "link", "prefix": "64", "address": "fe80::20c:29ff:fe09:ad42"}], "device": "eth0", "type": "ether"}, "ansible_python_version": "2.7.14", "ansible_product_name": "VMware Virtual Platform", "ansible_user_shell": "/bin/bash", "ansible_distribution_major_version": "6", "ansible_all_ipv4_addresses": ["192.168.177.128"], "ansible_nodename": "master"}}}
    '''
    for i in json.loads(aaaa):
        data =  ansible_caiji.collect(json.loads(aaaa)[i])
        # cores.Asset(data=data).create_asset()
        ass_handler = cores.Asset(data=data)
        ass_handler.data_inject()
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