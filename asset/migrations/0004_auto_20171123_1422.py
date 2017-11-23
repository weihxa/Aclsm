# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_auto_20171121_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
