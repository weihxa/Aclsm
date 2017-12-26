#_*_coding:utf-8_*_
__author__ = 'weihaoxuan'


from asset import models
import json

def get_asset_model(obj):
    asset_tables = ['server','networkdevice','software']
    for asset_type in asset_tables:
        if hasattr(obj,asset_type):
            ass_obj =getattr(obj,asset_type)
            return ass_obj.model
def fetch_asset_list():

    #asset_list = models.Asset.objects.values('id','idc__name','business_unit__name', 'manufactory__manufactory','server__model','asset_type','management_ip','cpu__cpu_model','sn','tags','name','networkdevice','trade_time')
    asset_list = models.Asset.objects.all()
    data_list = []
    for obj in asset_list:
        if hasattr(obj,'server') or hasattr(obj,'networkdevice'):
            if obj.asset_type == 'server':
                try:
                    cpu_model = obj.cpu.cpu_model
                    cpu_core_count = obj.cpu.cpu_core_count
                except Exception,e:
                    cpu_model = None
                    cpu_core_count = None
                data = {
                    'sn': obj.sn,
                    'name': obj.name,
                    'id': obj.id,
                    'idc': None if not obj.idc else obj.idc.name,
                    'business_unit': None if not obj.business_unit else obj.business_unit.name,
                    'manufactory': None if not obj.manufactory else obj.manufactory.manufactory,
                    'model': get_asset_model(obj),
                    'cpu_model' : cpu_model,
                    'cpu_core_count' : cpu_core_count,
                    'asset_type': obj.get_asset_type_display(),
                    'management_ip': obj.management_ip,
                    'ram_size': format(float(obj.mem_total/1024),'.2f'),
                    'disk_size': obj.disk_total,
                    'status': obj.get_status_display(),
                    'cabinet': None if not obj.cabinet else obj.cabinet.name,
                }
            elif obj.asset_type in ('switch','router','firewall','storage','NLB','wireless'):
                data = {
                    'sn': obj.sn,
                    'name': obj.name,
                    'id': obj.id,
                    'idc': None if not obj.idc else obj.idc.name,
                    'business_unit': None if not obj.business_unit else obj.business_unit.name,
                    'manufactory': None if not obj.manufactory else obj.manufactory.manufactory,
                    'model': get_asset_model(obj),
                    'cpu_model' : None,
                    'cpu_core_count' : None ,
                    'asset_type': obj.get_asset_type_display(),
                    'management_ip': obj.management_ip,
                    'ram_size': None,
                    'disk_size': None,
                    'status': None,
                    'cabinet': None ,
                }
            # print(data)
            #     data_list.append(data)
            elif obj.asset_type == 'Knifebox':
                    try:
                        cpu_model = obj.cpu.cpu_model
                        cpu_core_count = obj.cpu.cpu_core_count
                    except Exception, e:
                        cpu_model = None
                        cpu_core_count = None
                    data = {
                        'sn': obj.sn,
                        'name': obj.name,
                        'id': obj.id,
                        'idc': None if not obj.idc else obj.idc.name,
                        'business_unit': None if not obj.business_unit else obj.business_unit.name,
                        'manufactory': None if not obj.manufactory else obj.manufactory.manufactory,
                        'model': get_asset_model(obj),
                        'cpu_model': cpu_model,
                        'cpu_core_count': cpu_core_count,
                        'asset_type': obj.get_asset_type_display(),
                        'management_ip': obj.management_ip,
                        'ram_size': format(float(obj.mem_total/1024),'.2f'),
                        'disk_size': obj.disk_total,
                        'status': obj.get_status_display(),
                        'cabinet': None if not obj.cabinet else obj.cabinet.name,
                    }
            data_list.append(data)
    return  {'data':data_list}


def fetch_asset_Knifebox_logs(asset_id):
    log_list = models.Knifebox.objects.filter(asset_id= asset_id)
    data_list = []
    for log in log_list:
        data = {
            'id':log.id,
            'name':log.name,
            'Intranet_ip':log.Intranet_ip,
            'Outside_ip':log.Outside_ip,
            'memo':log.memo,
        }
        data_list.append(data)

    return {"data":data_list}

class AssetCategroy(object):
    def __init__(self,request):
        self.request = request
        self.category_type = request.GET.get("category_type")
        print('-->category type:',self.category_type)
    def serialize_data(self):

        if hasattr(self,str(self.category_type)):
            categroy_func = getattr(self,self.category_type)
            data = categroy_func()
        else:
            data = self.by_asset_type()

        return  data

    def by_idc(self):
        tree = []
        idc_list= models.IDC.objects.all()
        #asset_list = models.Asset.objects.all()
        for idc in idc_list:

            asset_type_dic = {}
            asset_list = idc.asset_set.select_related()
            idc_node = {
                "text":"%s(%s)" %(idc.name,len(asset_list)),
                "id": idc.id,
                "nodes":[]
            }

            for asset_type,asset_type_display_name in models.Asset.asset_type_choices:
                node_objs = asset_list.filter(asset_type=asset_type)
                node_dic =  {
                              "text"   :"%s(%s)" %(asset_type_display_name,len(node_objs)),
                              "id"     :asset_type,
                              'nodes'  :[],

                            }
                for node in node_objs:
                    node_dic["nodes"].append({"text":node.name,
                                              "id":node.id,
                                              "icon": "glyphicon glyphicon-stop",
                                              "selectedIcon": "glyphicon glyphicon-stop",
                                              })


                idc_node['nodes'].append(node_dic)
            tree.append(idc_node)

        return json.dumps(tree)

    def by_tag(self):
        tree = []
        tag_list = models.Tag.objects.all()
        for tag in tag_list:
            asset_list = tag.asset_set.select_related()
            first_layer_node = {
                "text":"%s(%s)" %(tag.name,len(asset_list)),
                "id": tag.id,
                "nodes":[]
            }

            for node in asset_list:
                first_layer_node["nodes"].append({"text":node.name,
                                          "id":node.id,
                                          "icon": "glyphicon glyphicon-stop",
                                          "selectedIcon": "glyphicon glyphicon-stop",
                                          })


            tree.append(first_layer_node)
        return json.dumps(tree)
    def by_asset_type(self):

        tree = []
        asset_type_dic = {}
        asset_list = models.Asset.objects.all()
        for asset_type,asset_type_display_name in models.Asset.asset_type_choices:
            node_objs = asset_list.filter(asset_type=asset_type)
            node_dic =  {
                          "text"   :"%s(%s)" %(asset_type_display_name,len(node_objs)),
                          "id"     :asset_type,
                          'nodes'  :[],

                        }
            for node in node_objs:
                node_dic["nodes"].append({"text":node.name,
                                          "id":node.id,
                                          "icon": "glyphicon glyphicon-stop",
                                          "selectedIcon": "glyphicon glyphicon-stop",
                                          })

            tree.append(node_dic)


        return json.dumps(tree)