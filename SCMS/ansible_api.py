#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

from ansible.runner import Runner
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import os


project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class MyRunner(object):
    def __init__(self,become_pass):
        self.__become_pass = become_pass

    def cmdrun(self,module_name='shell', module_args='', timeout=30, forks=10,
            pattern='*',become=False, become_user='root', transport='paramiko'):
        '''
        执行命令
        :return:
        '''
        hoc = Runner(host_list=os.path.join(project_dir,'temp','hosts'),
                     module_name=module_name,
                     module_args=module_args,
                     timeout=timeout,
                     pattern=pattern,
                     forks=forks,
                     become=become,
                     remote_user=become_user,
                     remote_pass = self.__become_pass,
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
            host_list=os.path.join(project_dir, 'temp', 'hosts'),
            playbook=play,
            stats=stats,
            callbacks=playbook_cb,
            timeout=timeout,
            forks=forks,
            runner_callbacks=runner_cb,
            remote_user=become_user,
            remote_pass=self.__become_pass,
            check=False,
            extra_vars=eval(params)
        )
        return pb.run()