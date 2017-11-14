#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django.contrib import admin
from asset import models
# from Integrated.user_admin import UserAdmin
# Register your models here.
# from django.contrib.auth.models import Group


class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    readonly_fields = ['create_date']

class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']
class NICInline(admin.TabularInline):
    model = models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']


class KnifeboxInline(admin.TabularInline):
    model = models.Knifebox
    exclude = ('memo',)
    readonly_fields = ['create_date']
class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']
class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','asset_type','sn','name','manufactory','management_ip','idc','cabinet','business_unit','status')
    inlines = [ServerInline,CPUInline,RAMInline,DiskInline,NICInline,KnifeboxInline]
    search_fields = ['sn',]
    list_filter = ['idc','cabinet','manufactory','business_unit','asset_type']
class NicAdmin(admin.ModelAdmin):
    list_display = ('name','macaddress','ipaddress','netmask','bonding')
    search_fields = ('macaddress','ipaddress')


class EventLogAdmin(admin.ModelAdmin):
    list_display = ('name','colored_event_type','asset','component','detail','date')
    search_fields = ('asset',)
    list_filter = ('event_type','component','date')



from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect




class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn','asset_type','manufactory','model','cpu_model','cpu_count','cpu_core_count','ram_size','os_distribution','os_release','date','approved','approved_date')
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "批准入库"

# Now register the new UserAdmin...
# admin.site.register(models.UserProfile,UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.IDC)
admin.site.register(models.Cabinet)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC,NicAdmin)
admin.site.register(models.RAM)
admin.site.register(models.Manufactory)
admin.site.register(models.Tag)
admin.site.register(models.Knifebox)
admin.site.register(models.Software)
admin.site.register(models.EventLog,EventLogAdmin)
admin.site.register(models.NewAssetApprovalZone,NewAssetApprovalZoneAdmin)
