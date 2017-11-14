# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knifebox',
            name='memo',
            field=models.CharField(max_length=64, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
    ]
