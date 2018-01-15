# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0008_jump_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='jump_logs',
            name='ipaddress',
            field=models.GenericIPAddressField(null=True, verbose_name='IP', blank=True),
        ),
    ]
