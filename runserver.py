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
from django.core.signals import request_started, request_finished
from django.contrib.sessions.models import Session
from Integrated.models import UserProfile
from jump import models as jump_models
from SCMS import models as scmd_models
import datetime,time
define('address', default='0.0.0.0', help='listen address')
define('port', default=8000, help='listen port', type=int)


project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))


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
            if session_key:
                session = get_object(Session, session_key=session_key)
                logging.info('Websocket: session: %s' % session)
                if session and datetime.datetime.now() < session.expire_date:
                    user_id = session.get_decoded().get('_auth_user_id')
                    request.user_id = user_id
                    user = get_object(UserProfile, email=user_id)
                    if user:
                        logging.info('Websocket: user [ %s ] request websocket' % user.username)
                        request.user = user
                        return func(request,request=request, *args, **kwargs)
                else:
                    logging.error('Websocket: session expired: %s' % session_key)
            try:
                request.close()
            except AttributeError:
                pass
            logging.error('Websocket: Request auth failed.')
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

    def get_hostname(self):
        return self.dst_addr.split(':')[0]

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
        if self.get_value('prem').strip() == 'root':
            args = (self.get_value('hostname'), 22, u'root', None, paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa'))
        else:
            p_user = jump_models.Jump_group.objects.filter(groupname=self.get_value('prem'))[0].user
            args = (self.get_value('hostname'), 22, str(p_user), None, paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa'))
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


    @django_request_support
    @require_auth('admin')
    def get(self,request,*args, **kwargs):
        if not request:
            return self.write('抱歉您的登陆失效过期请<a href="/login/">重新登陆</a>')
        else:
            items = self.get_value('hostname')
            self.__username = request.user
            try:
                if self.get_value('prem') == 'root' and request.user.is_admin:
                    if items.strip() not in scmd_models.device_config.objects.all().values_list('ipaddress',flat=True):
                        return self.write('抱歉您链接的机器不在ansible列表中，请<a href="/jump/lists">返回服务器列表页</a>')
                    self.render('xterm.html', items=items)
                group_data = jump_models.Jump_prem.objects.filter(username=request.user)[0].group
                if self.get_value('prem').strip() != str(group_data).strip():
                    return self.write('对不起您链接的组和您绑定权限不一致，请<a href="/jump/lists">返回服务器列表页</a>')
                dev_list = jump_models.Jump_group.objects.filter(groupname=group_data)[0].dev_list.split(',')
                if items.strip() not in dev_list:
                    return self.write('对不起您链接的机器和您绑定权限不一致，请<a href="/jump/lists">返回服务器列表页</a>')
            except Exception, e:
                logging.error(e)
                return self.write('发生未知错误，请<a href="/login/">重新登陆</a>')
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
        self.__log=[]
        self.__request = None
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
    @django_request_support
    @require_auth('admin')
    def open(self,request,*args, **kwargs):
        self.__request = request
        self.__filename = os.path.join(project_dir, 'jumplogs', str(int(time.time())) + 'jump.log')
        user = UserProfile.objects.get(email=str(request.user))
        jump_models.Jump_logs.objects.create(username=user,ipaddress=workers[self.get_argument('id')].get_hostname(),file_path=self.__filename)
        try:
            self.__openfile =  open(self.__filename,'w')
        except IOError,e:
            self.__openfile = False
            logging.error('日志存储目录未创建，无法存储日志。请创建jumplogs目录')
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
        if message == '\r' and not self.__openfile :
            self.__openfile.write(''.join(self.__log))
            self.__openfile.write('\n')
            self.__openfile.flush()
            self.__log = []
        else:
            self.__log.append(message)
        logging.debug('"{}" from {}'.format(message, self.src_addr))
        worker = self.worker_ref()
        worker.data_to_dst.append(message)
        worker.on_write()

    def on_close(self):
        self.__openfile.close()
        logging.info('Disconnected from {}'.format(self.src_addr))
        worker = self.worker_ref() if self.worker_ref else None
        if worker:
            worker.close()



def main():
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    settings = {
        'template_path': os.path.join(base_dir, 'templates'),
        'static_path': os.path.join(base_dir, 'static'),
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

