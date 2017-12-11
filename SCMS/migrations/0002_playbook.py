# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SCMS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playbook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='\u6587\u4ef6\u540d', blank=True)),
                ('description', models.CharField(max_length=1024, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('basedir', models.CharField(max_length=1024, null=True, verbose_name='\u5b58\u50a8\u8def\u5f84', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'playbook\u8bb0\u5f55',
                'verbose_name_plural': 'playbook\u8bb0\u5f55',
            },
        ),
    ]
