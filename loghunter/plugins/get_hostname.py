#!/usr/bin/env python
# -*- coding: utf8 -*-
import re



def get_hostname(ip):
    # fname = "/etc/hosts"
    fname = "E:/PycharmProjects/modify_hosts/hosts"
    f = open(fname)
    tmp_data = f.read()
    f.close()
    if ip:
        get_data = re.findall(r"%s\b(.*)" % ip, tmp_data)
        if len(get_data) > 1:
            return 2,"Wrong! %s Get more than one hostname!" % ip
        elif len(get_data) == 0:
            return 1,"%s Have no hostname!" % ip
        else:
            return 0,''.join(get_data).strip()
    return "IP is empty!!!!"

def get_ip(hostname):
    fname = "E:/PycharmProjects/modify_hosts/hosts"
    f = open(fname)
    tmp_data = f.read()
    f.close()
    if hostname:
        get_data = re.findall(r"(.*)%s\b" % hostname, tmp_data)
        if len(get_data) > 1:
            return 2, "Wrong! %s Get more than one ip!" % hostname
        elif len(get_data) == 0:
            return 1, "%s Have no ip!" % hostname
        else:
            return 0, ''.join(get_data).strip()
    return "Hostname is empty!!!!"



if __name__ == '__main__':
    print get_hostname('10.66.5.35')
    print get_ip('bjdx005sin035.hnapay.com')
