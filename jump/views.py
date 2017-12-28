#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect,StreamingHttpResponse
from django.contrib import auth
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from Integrated.plugins.Decorators import Perm_verification
import json
import models




@login_required
@Perm_verification(perm='jump')
def index(request):
    return render(request, 'jump/index.html',
                      context_instance=RequestContext(request))


@login_required
@Perm_verification(perm='jump')
def lists(request):
    return render(request, 'jump/lists.html',
                      context_instance=RequestContext(request))

@login_required
@Perm_verification(perm='jump')
def users(request):
    data = models.Jump_user.objects.all()
    return render(request, 'jump/users.html',{'data':data},
                      context_instance=RequestContext(request))