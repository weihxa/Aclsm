# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0002_auto_20171228_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='jump_user',
            name='password',
            field=models.CharField(max_length=30, null=True, verbose_name='\u8d26\u6237\u5bc6\u7801', blank=True),
        ),
    ]
