# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlog',
            name='asset',
        ),
        migrations.DeleteModel(
            name='NewAssetApprovalZone',
        ),
        migrations.RemoveField(
            model_name='networkdevice',
            name='firmware',
        ),
        migrations.RemoveField(
            model_name='server',
            name='raid_type',
        ),
        migrations.DeleteModel(
            name='EventLog',
        ),
        migrations.DeleteModel(
            name='Software',
        ),
    ]
