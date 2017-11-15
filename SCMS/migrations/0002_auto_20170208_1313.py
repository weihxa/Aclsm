# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SCMS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group_config',
            name='group_pc_num',
        ),
        migrations.AddField(
            model_name='group_config',
            name='nginx_puth',
            field=models.CharField(max_length=128, null=True, verbose_name='\u63a8\u9001nginx\u8def\u5f84', blank=True),
        ),
        migrations.AddField(
            model_name='group_config',
            name='tomcat_puth',
            field=models.CharField(max_length=128, null=True, verbose_name='\u63a8\u9001tomcat\u8def\u5f84', blank=True),
        ),
    ]
