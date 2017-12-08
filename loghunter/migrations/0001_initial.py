# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u4e3b\u673a')),
                ('mark', models.CharField(max_length=80, verbose_name='\u7a7a\u95f4')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u78c1\u76d8\u7a7a\u95f4',
                'verbose_name_plural': '\u78c1\u76d8\u7a7a\u95f4',
            },
        ),
        migrations.CreateModel(
            name='Early_warn',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('ipaddress', models.GenericIPAddressField(null=True, verbose_name='IP\u5730\u5740', blank=True)),
                ('mark', models.CharField(max_length=30, verbose_name='\u6545\u969c\u6807\u8bc6')),
                ('report_msm', models.TextField(verbose_name='\u6c47\u62a5\u4fe1\u606f')),
                ('report_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u5f02\u5e38\u6293\u53d6\u63a8\u9001',
                'verbose_name_plural': '\u5f02\u5e38\u6293\u53d6\u63a8\u9001',
            },
        ),
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
