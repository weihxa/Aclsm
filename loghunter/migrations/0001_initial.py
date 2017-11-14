# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Early_warn',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('ipaddress', models.GenericIPAddressField(null=True, verbose_name='IP\u5730\u5740', blank=True)),
                ('mark', models.CharField(max_length=30, verbose_name='\u6545\u969c\u6807\u8bc6')),
                ('report_msm', models.TextField(verbose_name='\u6c47\u62a5\u4fe1\u606f')),
                ('report_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u5f02\u5e38\u6293\u53d6\u63a8\u9001',
                'verbose_name_plural': '\u5f02\u5e38\u6293\u53d6\u63a8\u9001',
            },
        ),
    ]
