# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loghunter', '0006_auto_20170629_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='mark',
            field=models.CharField(max_length=80, verbose_name='\u7a7a\u95f4'),
        ),
    ]
