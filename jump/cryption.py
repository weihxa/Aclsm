#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import base64
import pyDes

Des_Key = "BMWd\n0#\x43"
Des_IV = "W\x23f\0\t1@\n"

def encryption(str):
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None, padmode=pyDes.PAD_PKCS5)
    EncryptStr = k.encrypt(str)
    return base64.b64encode(EncryptStr)
def decrypt(str):
    data = base64.b64decode(str)
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None, padmode=pyDes.PAD_PKCS5)
    EncryptStr = k.decrypt(data)
    return EncryptStr
