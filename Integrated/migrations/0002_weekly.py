# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Integrated', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weekly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weeklys', models.CharField(max_length=128, null=True, verbose_name='\u91cd\u70b9\u5de5\u4f5c\u4e8b\u9879', blank=True)),
                ('workplan', models.CharField(max_length=128, null=True, verbose_name='\u5de5\u4f5c\u8ba1\u5212', blank=True)),
                ('completion', models.CharField(max_length=128, null=True, verbose_name='\u672c\u5468\u8ba1\u5212\u5b8c\u6210\u60c5\u51b5', blank=True)),
                ('coordination', models.CharField(max_length=128, null=True, verbose_name='\u5de5\u4f5c\u96be\u70b9\u53ca\u6240\u9700\u534f\u8c03\u7684\u8d44\u6e90', blank=True)),
                ('nextweek', models.CharField(max_length=128, null=True, verbose_name='\u4e0b\u5468\u5de5\u4f5c\u8ba1\u5212', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.ForeignKey(verbose_name='\u7528\u6237\u540d', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5de5\u4f5c\u8ba1\u5212',
                'verbose_name_plural': '\u5de5\u4f5c\u8ba1\u5212',
            },
        ),
    ]
