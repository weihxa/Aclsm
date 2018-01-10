#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
import io
import logging
import os.path
import socket
import traceback
import uuid
import functools
import weakref
import paramiko
import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop
from tornado.iostream import _ERRNO_CONNRESET
from tornado.options import define, options, parse_command_line
from tornado.util import errno_from_exception
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xbmanIntegrated.settings")
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from django.contrib.auth.decorators import login_required
from xbmanIntegrated import settings
from Integrated import models
from django.core.signals import request_started, request_finished
from importlib import import_module
from django.contrib import auth
from django.contrib.sessions.models import Session
from Integrated.models import UserProfile
import time
import datetime
define('address', default='127.0.0.1', help='listen address')
define('port', default=8000, help='listen port', type=int)

import django.contrib.sessions.backends.db
BUF_SIZE = 1024
DELAY = 3
base_dir = os.path.dirname(__file__)
workers = {}

def django_request_support(func):
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        request_started.send_robust(func)
        response = func(*args, **kwargs)
        request_finished.send_robust(func)
        print response
        return response

    return _deco

def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object

def require_auth(role='user'):
    def _deco(func):
        def _deco2(request, *args, **kwargs):
            if request.get_cookie('sessionid'):
                session_key = request.get_cookie('sessionid')
            else:
                session_key = request.get_argument('sessionid', '')

            print('Websocket: session_key: %s' % session_key)
            if session_key:
                session = get_object(Session, session_key=session_key)
                print('Websocket: session: %s' % session)
                if session and datetime.datetime.now() < session.expire_date:
                    user_id = session.get_decoded().get('_auth_user_id')
                    print user_id
                    request.user_id = user_id
                    user = get_object(UserProfile, email=user_id)
                    if user:
                        print('Websocket: user [ %s ] request websocket' % user.username)
                        request.user = user
                        print request
                        return func(request,request=request, *args, **kwargs)
                else:
                    print('Websocket: session expired: %s' % session_key)
            try:
                request.close()
            except AttributeError:
                pass
            print('Websocket: Request auth failed.')
            return func(request, request=None, *args, **kwargs)

        return _deco2

    return _deco

def recycle(worker):
    if worker.handler:
        return
    logging.debug('Recycling worker {}'.format(worker.id))
    workers.pop(worker.id, None)
    worker.close()


class Worker(object):
    def __init__(self, ssh, chan, dst_addr):
        self.loop = IOLoop.current()
        self.ssh = ssh
        self.chan = chan
        self.dst_addr = dst_addr
        self.fd = chan.fileno()
        self.id = str(id(self))
        self.data_to_dst = []
        self.handler = None
        self.mode = IOLoop.READ

    def __call__(self, fd, events):
        if events & IOLoop.READ:
            self.on_read()
        if events & IOLoop.WRITE:
            self.on_write()
        if events & IOLoop.ERROR:
            self.close()

    def set_handler(self, handler):
        if not self.handler:
            self.handler = handler

    def update_handler(self, mode):
        if self.mode != mode:
            self.loop.update_handler(self.fd, mode)
            self.mode = mode

    def on_read(self):
        logging.debug('worker {} on read'.format(self.id))
        try:
            data = self.chan.recv(BUF_SIZE)
        except (OSError, IOError) as e:
            logging.error(e)
            if errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close()
        else:
            logging.debug('"{}" from {}'.format(data, self.dst_addr))
            if not data:
                self.close()
                return

            logging.debug('"{}" to {}'.format(data, self.handler.src_addr))
            try:
                self.handler.write_message(data)
            except tornado.websocket.WebSocketClosedError:
                self.close()

    def on_write(self):
        logging.debug('worker {} on write'.format(self.id))
        if not self.data_to_dst:
            return

        data = ''.join(self.data_to_dst)
        logging.debug('"{}" to {}'.format(data, self.dst_addr))

        try:
            sent = self.chan.send(data)
        except (OSError, IOError) as e:
            logging.error(e)
            if errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close()
            else:
                self.update_handler(IOLoop.WRITE)
        else:
            self.data_to_dst = []
            data = data[sent:]
            if data:
                self.data_to_dst.append(data)
                self.update_handler(IOLoop.WRITE)
            else:
                self.update_handler(IOLoop.READ)

    def close(self):
        logging.debug('Closing worker {}'.format(self.id))
        if self.handler:
            self.loop.remove_handler(self.fd)
            self.handler.close()
        self.chan.close()
        self.ssh.close()
        logging.info('Connection to {} lost'.format(self.dst_addr))


class IndexHandler(tornado.web.RequestHandler):
    def get_privatekey(self):
        try:
            data = self.request.files.get('privatekey')[0]['body']
        except TypeError:
            return
        return data.decode('utf-8')

    def get_specific_pkey(self, pkeycls, privatekey, password):
        logging.info('Trying {}'.format(pkeycls.__name__))
        try:
            pkey = pkeycls.from_private_key(io.StringIO(privatekey),
                                            password=password)
        except paramiko.PasswordRequiredException:
            raise ValueError('Need password to decrypt the private key.')
        except paramiko.SSHException:
            pass
        else:
            return pkey

    def get_pkey(self, privatekey, password):
        password = password.encode('utf-8') if password else None

        pkey = self.get_specific_pkey(paramiko.RSAKey, privatekey, password)\
            or self.get_specific_pkey(paramiko.DSSKey, privatekey, password)\
            or self.get_specific_pkey(paramiko.ECDSAKey, privatekey, password)\
            or self.get_specific_pkey(paramiko.Ed25519Key, privatekey,
                                      password)
        if not pkey:
            raise ValueError('Not a valid private key file or '
                             'wrong password for decrypting the private key.')
        return pkey

    def get_port(self):
        value = self.get_value('port')
        try:
            port = int(value)
        except ValueError:
            port = 0

        if 0 < port < 65536:
            return port

        raise ValueError('Invalid port {}'.format(value))

    def get_value(self, name):
        value = self.get_argument(name)
        if not value:
            raise ValueError('Empty {}'.format(name))
        return value

    def get_args(self):
        hostname = self.get_value('hostname')
        port = self.get_port()
        username = self.get_value('username')
        password = self.get_argument('password')
        privatekey = self.get_privatekey()
        pkey = self.get_pkey(privatekey, password) if privatekey else None
        args = (hostname, port, username, password, pkey)
        logging.debug(args)
        return args

    def ssh_connect(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # args = self.get_args()
        args = (u'192.168.177.129', 22, u'root', None, paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa'))
        print args
        dst_addr = '{}:{}'.format(*args[:2])
        logging.info('Connecting to {}'.format(dst_addr))
        try:
            ssh.connect(*args, timeout=6)
        except socket.error:
            raise ValueError('Unable to connect to {}'.format(dst_addr))
        except paramiko.BadAuthenticationType:
            raise ValueError('Authentication failed.')
        chan = ssh.invoke_shell(term='xterm')
        chan.setblocking(0)
        worker = Worker(ssh, chan, dst_addr)
        IOLoop.current().call_later(DELAY, recycle, worker)
        return worker

    # def get_current_user(self):
    #     self.session_key = self.get_cookie('sessionid')
    #     engine = import_module(settings.SESSION_ENGINE)
    #     session = engine.SessionStore(self.session_key)
    #     print session
    #     # r = DummyRequest()
    #     # r.session = session
    #     self.user = auth.get_user(session)
    #     return self.user

    @django_request_support
    @require_auth('admin')
    def get(self,request,*args, **kwargs):
        print 'nihao'
        print request
        if not request:
            self.write('抱歉您的登陆失效过期请<a href="/login/">重新登陆</a>')
        else:
            print 'dsdsdfsdfsdf'
            items = '1.1.1.1'
            print self.get_value('username')
            print self.get_cookie('sessionid')
            self.render('xterm.html', items=items)

    def post(self):
        worker_id = None
        status = None

        try:
            worker = self.ssh_connect()
        except Exception as e:
            logging.error(traceback.format_exc())
            status = str(e)
        else:
            worker_id = worker.id
            workers[worker_id] = worker

        self.write(dict(id=worker_id, status=status))


class WsockHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        self.loop = IOLoop.current()
        self.worker_ref = None
        super(self.__class__, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def get_addr(self):
        ip = self.request.headers.get_list('X-Real-Ip')
        port = self.request.headers.get_list('X-Real-Port')
        addr = ':'.join(ip + port)
        if not addr:
            addr = '{}:{}'.format(*self.stream.socket.getpeername())
        return addr

    def open(self):
        self.src_addr = self.get_addr()
        logging.info('Connected from {}'.format(self.src_addr))
        worker = workers.pop(self.get_argument('id'), None)
        if not worker:
            self.close(reason='Invalid worker id')
            return
        self.set_nodelay(True)
        worker.set_handler(self)
        self.worker_ref = weakref.ref(worker)
        self.loop.add_handler(worker.fd, worker, IOLoop.READ)

    def on_message(self, message):
        logging.debug('"{}" from {}'.format(message, self.src_addr))
        worker = self.worker_ref()
        worker.data_to_dst.append(message)
        worker.on_write()

    def on_close(self):
        logging.info('Disconnected from {}'.format(self.src_addr))
        worker = self.worker_ref() if self.worker_ref else None
        if worker:
            worker.close()

    # def get_current_user(self):
    #     self.session_key = self.get_cookie('sessionid')
    #     engine = import_module(settings.SESSION_ENGINE)
    #     session = engine.SessionStore(self.session_key)
    #     print session
    #     # r = DummyRequest()
    #     # r.session = session
    #     # self.user = auth.get_user(r)
    #     # return self.user


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    settings = {
        'template_path': os.path.join(base_dir, 'templates'),
        'static_path': os.path.join(base_dir, 'static'),
        # 'cookie_secret': uuid.uuid1().hex,
        # 'debug': True
    }

    handlers = [
        (r'/xterm/',IndexHandler),
        (r'/ws', WsockHandler),
        (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
         dict(path=os.path.join(os.path.dirname(__file__), "static"))),
    ]

    parse_command_line()
    app = tornado.web.Application(handlers, **settings)
    app.listen(options.port, options.address)
    logging.info('Listening on {}:{}'.format(options.address, options.port))
    IOLoop.current().start()


if __name__ == '__main__':
    main()
