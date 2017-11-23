# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='status',
            field=models.IntegerField(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81'),
        ),
    ]
