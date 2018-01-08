# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0004_jump_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jump_prem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30, null=True, verbose_name='\u7528\u6237\u540d', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(verbose_name='\u7ed1\u5b9a\u7ec4', blank=True, to='jump.Jump_group', null=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6743\u9650\u7ed1\u5b9a\u8868',
                'verbose_name_plural': '\u7528\u6237\u6743\u9650\u7ed1\u5b9a\u8868',
            },
        ),
    ]
