# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jump', '0007_jump_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jump_logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=30, null=True, verbose_name='\u65e5\u5fd7\u6587\u4ef6\u8def\u5f84', blank=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('username', models.ForeignKey(verbose_name='\u7528\u6237\u540d', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u65e5\u5fd7\u8868',
                'verbose_name_plural': '\u65e5\u5fd7\u8868',
            },
        ),
    ]
