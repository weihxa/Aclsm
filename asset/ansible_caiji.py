#_*_coding:utf-8_*_
__author__ = 'weihaoxuan'


def collect(image):

    data = {"asset_type":'server'}
    data['manufactory'] = image['ansible_facts']['ansible_system_vendor']
    data['sn'] = image['ansible_facts']['ansible_product_serial']
    data['model'] = image['ansible_facts']['ansible_product_name']
    data['uuid'] = image['ansible_facts']['ansible_product_uuid']
    data['mem_total'] = image['ansible_facts']['ansible_memtotal_mb']
    data['wake_up_type'] = 'Power Switch'

    data.update(cpuinfo(image['ansible_facts']))
    data.update(osinfo(image['ansible_facts']))
    data.update({'ram':[]})
    data.update(nicinfo(image['ansible_facts']))
    data.update(diskinfo(image['ansible_facts']))
    return data


def diskinfo(img):
    disk_dic = {}
    sum = 0
    for i in img['ansible_devices']:
        if i not in disk_dic:
            d_sum = int(img['ansible_devices'][i]['sectors'])*int(img['ansible_devices'][i]['sectorsize']) / 1024 / 1024 / 1024
            sum = sum + d_sum
            disk_dic[i] = {'slot': i,
                                 'capacity': d_sum,
                                 'manufactory': img['ansible_devices'][i]['vendor'],
                                 'sn': img['ansible_devices'][i]['host'],
                                 'iface_type': 0,
                                 'model': 'unknown',
                                 }


    disk_list = []
    for k, v in disk_dic.items():
        disk_list.append(v)
    return {'physical_disk_driver':disk_list,'disk_total':sum}

def nicinfo(img):
    nic_dic = {}
    for i in img["ansible_interfaces"]:
        if i == 'lo':
            continue
        if img["ansible_%s"%i]['macaddress'] not in nic_dic:
            nic_dic[img["ansible_%s"%i]['macaddress']] = {'name': img["ansible_%s"%i]['device'],
                                 'macaddress': img["ansible_%s"%i]['macaddress'],
                                 'netmask': img["ansible_%s"%i]['ipv4']['netmask'],
                                 'network': img["ansible_%s"%i]['ipv4']['network'],
                                 'bonding': 0,
                                 'model': 'unknown',
                                 'ipaddress': img["ansible_%s"%i]['ipv4']['address'],
                                 }

    nic_list= []
    for k,v in nic_dic.items():
        nic_list.append(v)

    return {'nic':nic_list}

def osinfo(img):
    distributor = img["ansible_distribution"].strip()
    release  = img["ansible_distribution_version"].strip()
    data_dic ={
        "os_distribution": distributor if len(distributor)>1 else None,
        "os_release":release if len(release)>1 else None,
        "os_type": img["ansible_system"]
    }
    return data_dic
def cpuinfo(img):

    data = {
        "cpu_count" : img["ansible_processor_cores"],
        "cpu_core_count": img["ansible_processor_vcpus"],
        "cpu_model" : img["ansible_processor"][1]
        }
    return data


if __name__=="__main__":
    exit()