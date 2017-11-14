# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loghunter', '0003_disk_create_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='softver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u4e3b\u673a')),
                ('Kernel', models.CharField(max_length=80, verbose_name='\u5185\u6838')),
                ('nginx', models.CharField(max_length=80, verbose_name='nginx')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u8f6f\u4ef6\u7248\u672c',
                'verbose_name_plural': '\u8f6f\u4ef6\u7248\u672c',
            },
        ),
    ]
