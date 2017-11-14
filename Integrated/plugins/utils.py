#_*_coding:utf-8_*_
__author__ = 'weihaoxuan'

import time,hashlib,json
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from Integrated import models

def gen_token(username,timestamp,token):
    token_format = "%s\n%s\n%s" %(username,timestamp,token)
    obj = hashlib.md5()
    obj.update(token_format)
    return obj.hexdigest()[10:17]


def token_required(func):
    def wrapper(*args,**kwargs):
        response = {"errors":[]}

        get_args = args[0].GET
        username = get_args.get("user")
        token_md5_from_client = get_args.get("token")
        timestamp = get_args.get("timestamp")
        if not username or not timestamp or not token_md5_from_client:
            response['errors'].append({"auth_failed":"This api requires token authentication!"})
            return HttpResponse(json.dumps(response))
        try:
            user_obj = models.UserProfile.objects.get(email=username)
            token_md5_from_server = gen_token(username,timestamp,user_obj.token)
            if token_md5_from_client != token_md5_from_server:
                response['errors'].append({"auth_failed":"Invalid username or token_id"})
            else:
                if abs(time.time() - int(timestamp)) > 120:# default timeout 120
                    response['errors'].append({"auth_failed":"The token is expired!"})
                else:
                    pass
        except ObjectDoesNotExist as e:
            response['errors'].append({"auth_failed":"Invalid username or token_id"})
        if response['errors']:
            return HttpResponse(json.dumps(response))
        else:
            return  func(*args,**kwargs)
    return wrapper