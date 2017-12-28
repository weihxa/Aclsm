# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jump_user',
            name='username',
            field=models.CharField(max_length=30, null=True, verbose_name='\u8d26\u6237\u540d\u79f0', blank=True),
        ),
    ]
