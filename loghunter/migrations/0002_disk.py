# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loghunter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u4e3b\u673a')),
                ('mark', models.CharField(max_length=80, verbose_name='\u7a7a\u95f4')),
            ],
            options={
                'verbose_name': '\u78c1\u76d8\u7a7a\u95f4',
                'verbose_name_plural': '\u78c1\u76d8\u7a7a\u95f4',
            },
        ),
    ]
