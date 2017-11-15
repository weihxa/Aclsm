# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='configuration_file',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=32, verbose_name='\u663e\u793a\u540d', blank=True)),
                ('file_content', models.TextField(max_length=256, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6', blank=True)),
                ('mark', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u6807\u8bc6', choices=[(b'1', 'nginx'), (b'2', 'tomcat'), (b'3', 'nginxinstall'), (b'4', 'tomcatinstall')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u914d\u7f6e\u6587\u4ef6\u8868',
                'verbose_name_plural': '\u914d\u7f6e\u6587\u4ef6\u8868',
            },
        ),
        migrations.CreateModel(
            name='device_config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=64, verbose_name='\u63cf\u8ff0', blank=True)),
                ('ipaddress', models.GenericIPAddressField(null=True, verbose_name='IP', blank=True)),
                ('password', models.CharField(max_length=128, verbose_name='\u5bc6\u7801', blank=True)),
                ('memo', models.CharField(max_length=64, null=True, verbose_name='\u914d\u7f6e', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='group_config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=64, verbose_name='\u7ec4\u540d', blank=True)),
                ('group_pc_num', models.IntegerField(null=True, verbose_name='\u7ec4\u5185\u673a\u5668\u6570', blank=True)),
                ('description', models.TextField(max_length=64, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u7ec4\u4fe1\u606f',
                'verbose_name_plural': '\u7ec4\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='group_device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=64, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('device_name', models.ForeignKey(verbose_name='\u673a\u5668\u540d', to='SCMS.device_config')),
                ('group_name', models.ForeignKey(verbose_name='\u7ec4\u540d', to='SCMS.group_config')),
            ],
            options={
                'verbose_name': '\u7ec4\u548c\u6210\u5458\u5bf9\u7167\u8868',
                'verbose_name_plural': '\u7ec4\u548c\u6210\u5458\u5bf9\u7167\u8868',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rpm_name', models.CharField(max_length=64, verbose_name='\u8f6f\u4ef6\u5305\u540d', blank=True)),
                ('headImg', models.FileField(upload_to=b'./upload/')),
                ('description', models.TextField(max_length=64, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u8f6f\u4ef6\u5305\u8868',
                'verbose_name_plural': '\u8f6f\u4ef6\u5305\u8868',
            },
        ),
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=64, null=True, verbose_name='\u4efb\u52a1\u540d', blank=True)),
                ('task_Operated', models.CharField(max_length=1024, null=True, verbose_name='\u88ab\u64cd\u4f5cIP\u6216\u7ec4\u540d', blank=True)),
                ('config_name', models.CharField(max_length=128, null=True, verbose_name='\u88ab\u63a8\u9001\u914d\u7f6e\u6587\u4ef6\u540d', blank=True)),
                ('task_log', models.TextField(max_length=2048, null=True, verbose_name='\u64cd\u4f5c\u65e5\u5fd7')),
                ('task_result', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u64cd\u4f5c\u7ed3\u679c', choices=[(b'1', '\u6210\u529f'), (b'2', '\u5931\u8d25'), (b'3', '\u8fdb\u884c\u4e2d')])),
            ],
            options={
                'verbose_name': '\u64cd\u4f5c\u8bb0\u5f55\u8868',
                'verbose_name_plural': '\u64cd\u4f5c\u8bb0\u5f55\u8868',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1')),
                ('name', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('token', models.CharField(default=None, max_length=128, null=True, verbose_name='token', blank=True)),
                ('department', models.CharField(default=None, max_length=32, null=True, verbose_name='\u90e8\u95e8', blank=True)),
                ('tel', models.CharField(default=None, max_length=32, null=True, verbose_name='\u5ea7\u673a', blank=True)),
                ('mobile', models.CharField(default=None, max_length=32, null=True, verbose_name='\u624b\u673a', blank=True)),
                ('memo', models.TextField(default=None, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('valid_begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_end_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u7528\u6237\u4fe1\u606f\u8868',
            },
        ),
        migrations.AddField(
            model_name='device_config',
            name='group',
            field=models.ManyToManyField(to='SCMS.group_config', verbose_name='\u5c5e\u7ec4', blank=True),
        ),
    ]
