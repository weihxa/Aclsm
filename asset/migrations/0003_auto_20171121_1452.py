# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20171121_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='disk_total',
            field=models.FloatField(null=True, verbose_name='\u786c\u76d8\u603b\u91cf(G)', blank=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='mem_total',
            field=models.FloatField(null=True, verbose_name='\u5185\u5b58\u603b\u91cf(G)', blank=True),
        ),
    ]
