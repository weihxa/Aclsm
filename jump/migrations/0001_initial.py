# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jump_user',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.GenericIPAddressField(null=True, verbose_name='\u8d26\u6237\u540d\u79f0', blank=True)),
                ('permiss', models.TextField(verbose_name='sudo\u6743\u9650')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u8fdc\u7a0b\u8d26\u6237\u8868',
                'verbose_name_plural': '\u8fdc\u7a0b\u8d26\u6237\u8868',
            },
        ),
    ]
