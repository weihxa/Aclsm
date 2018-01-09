#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

from ansible.runner import Runner
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import os
import paramiko

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class MyRunner(object):

    def __init__(self):
        pass

    def cmdrun(self,module_name='shell', module_args='', timeout=30, forks=10,
            pattern='*',become=False, become_user='root', transport='paramiko'):
        '''
        执行命令
        :return:
        '''
        hoc = Runner(
             host_list=os.path.join(project_dir, 'temp', 'hosts'),
             module_name=module_name,
             module_args=module_args,
             timeout=timeout,
             pattern=pattern,
             forks=forks,
             become=become,
             remote_user=become_user,
             transport=transport
             )
        results_raw = hoc.run()
        return results_raw

    def PlayBook_execute(self,play, params,timeout=30, forks=10, become_user='root'):
        '''
        执行playbook模块
        '''
        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        pb = PlayBook(
            playbook=play,
            stats=stats,
            callbacks=playbook_cb,
            timeout=timeout,
            forks=forks,
            runner_callbacks=runner_cb,
            remote_user=become_user,
            check=False,
            extra_vars=eval(params)
            )
        return pb.run()
    def roles_execute(self,play,timeout=30, forks=10, become_user='root',inventory=os.path.join(project_dir, 'temp', 'hosts')):
        '''
        执行playbook模块
        '''
        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        pb = PlayBook(
            playbook=play,
            host_list=inventory,
            stats=stats,
            callbacks=playbook_cb,
            timeout=timeout,
            forks=forks,
            runner_callbacks=runner_cb,
            remote_user=become_user,
            check=False
            )
        return pb.run()
    def deploy_key(self,server, username, password):
        '''
        添加KEY
        :param server: ip
        :param username: root?
        :param password: ??
        :return:
        '''
        try:
            key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, username=username, password=password)
            client.exec_command('mkdir -p ~/.ssh/')
            client.exec_command('touch ~/.ssh/authorized_keys')
            client.exec_command('echo "%s" >> ~/.ssh/authorized_keys' % key)
            client.exec_command('chmod 644 ~/.ssh/authorized_keys')
            client.exec_command('chmod 700 ~/.ssh/')
        except paramiko.ssh_exception.AuthenticationException, e:
            return (False,'密码错误！')
        except paramiko.ssh_exception.NoValidConnectionsError, e:
            return (False,'主机链接不上!')
        else:
            return (True,'添加成功!')


if __name__ == "__main__":
    print MyRunner().roles_execute(play='/tmp/ansible-role-percona/repl_test.yml',
                                      inventory='/tmp/ansible-role-percona/inventory')
    print MyRunner().cmdrun(pattern='192.168.177.129',
                                                 module_args='echo "dsf" ')['contacted']