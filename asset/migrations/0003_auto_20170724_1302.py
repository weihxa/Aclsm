# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20170724_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knifebox',
            name='memo',
            field=models.CharField(max_length=64, null=True, verbose_name='\u5907\u6ce8'),
        ),
    ]
