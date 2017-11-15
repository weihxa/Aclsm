#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import os
import models

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class process(object):
    def __init__(self):
        pass
    def nginx_conf(self,id):
        # 生成nginx配置文件
        file_obj = models.configuration_file.objects.get(id=id)
        dirs = os.path.join(project_dir,'temp','date',file_obj.file_name)
        os.system('mkdir -p %s'%dirs)
        with open(dirs + '/nginx.conf', 'w') as f:
            f.write(file_obj.file_content)
        return file_obj.file_name,os.path.join(dirs,'nginx.conf')

    def tomcat_conf(self, id):
        # 生成tomcat配置文件
        file_obj = models.configuration_file.objects.get(id=id)
        dirs = os.path.join(project_dir, 'temp', 'date', file_obj.file_name)
        print dirs
        os.system('mkdir  -p %s' % dirs)
        with open(dirs + '/server.xml', 'w') as f:
            f.write(file_obj.file_content)
        return file_obj.file_name,os.path.join(dirs,'server.xml')

    def tomcatinstall_conf(self, id):
        # 生成nginx安装配置文件
        file_obj = models.configuration_file.objects.get(id=id)
        dirs = os.path.join(project_dir, 'temp', 'date', file_obj.file_name)
        os.system('mkdir %s -p' % dirs)
        with open(dirs + '/tomcat.yaml', 'w') as f:
            f.write(file_obj.file_content)
        return file_obj.file_name,os.path.join(dirs,'tomcat.yaml')

    def nginxinstall_conf(self, id):
        # 生成tomcat安装配置文件
        file_obj = models.configuration_file.objects.get(id=id)
        dirs = os.path.join(project_dir, 'temp', 'date', file_obj.file_name)
        os.system('mkdir %s -p' % dirs)
        with open(dirs + '/nginx.yaml', 'w') as f:
            f.write(file_obj.file_content)
        return file_obj.file_name,os.path.join(dirs,'nginx.yaml')