# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0005_jump_prem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jump_prem',
            name='username',
            field=models.ForeignKey(default=datetime.datetime(2018, 1, 8, 17, 23, 34, 486000), verbose_name='\u7528\u6237\u540d', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
