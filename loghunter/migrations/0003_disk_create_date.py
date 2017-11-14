# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('loghunter', '0002_disk'),
    ]

    operations = [
        migrations.AddField(
            model_name='disk',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 27, 19, 23, 36, 689000), auto_now_add=True),
            preserve_default=False,
        ),
    ]
