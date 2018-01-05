# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0003_jump_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jump_group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('groupname', models.CharField(max_length=30, null=True, verbose_name='\u7ec4\u540d\u79f0', blank=True)),
                ('dev_list', models.CharField(max_length=9999, null=True, verbose_name='\u673a\u5668', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(verbose_name='\u7ed1\u5b9a\u8d26\u53f7', blank=True, to='jump.Jump_user', null=True)),
            ],
            options={
                'verbose_name': '\u673a\u5668\u5206\u7ec4\u8868',
                'verbose_name_plural': '\u673a\u5668\u5206\u7ec4\u8868',
            },
        ),
    ]
