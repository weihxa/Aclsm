#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import paramiko

from xbmanIntegrated import settings


class modify_paramiko(object):
    def __init__(self,ip):
        self.__lvshostip = ip
        self.__port = settings.port
        self.__username = settings.username
        self.__password = settings.password


    def Landed(self,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.__lvshostip,self.__port,self.__username,self.__password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        OUT = stdout.read()
        ssh.close()
        return OUT

    def killtomcat(self, cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.__lvshostip, self.__port, self.__username, self.__password)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            OUT = stdout.readlines()
            ssh.close()
            return OUT
        except paramiko.ssh_exception.AuthenticationException, e:
            return '账号或密码错误'


if __name__ == '__main__':
    exit(1)