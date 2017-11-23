# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0007_auto_20171123_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
