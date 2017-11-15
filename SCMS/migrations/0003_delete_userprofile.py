# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SCMS', '0002_auto_20170208_1313'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
