# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loghunter', '0005_tomcatver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='mark',
            field=models.IntegerField(verbose_name='\u7a7a\u95f4'),
        ),
    ]
