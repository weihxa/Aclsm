# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0006_auto_20171123_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='create_date',
            field=models.DateField(default=django.utils.timezone.now, blank=True),
        ),
    ]
