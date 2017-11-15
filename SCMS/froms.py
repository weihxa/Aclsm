#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'
from django import forms

class headImg(forms.Form):
    headImg = forms.FileField()