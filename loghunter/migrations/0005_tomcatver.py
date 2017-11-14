# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loghunter', '0004_softver'),
    ]

    operations = [
        migrations.CreateModel(
            name='tomcatver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u4e3b\u673a')),
                ('tomcat', models.CharField(max_length=80, verbose_name='\u7248\u672c')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'tomcat\u7248\u672c',
                'verbose_name_plural': 'tomcat\u7248\u672c',
            },
        ),
    ]
