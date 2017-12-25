# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_type', models.CharField(default=b'server', max_length=64, choices=[(b'server', '\u670d\u52a1\u5668'), (b'Knifebox', '\u5200\u7bb1'), (b'switch', '\u4ea4\u6362\u673a'), (b'router', '\u8def\u7531\u5668'), (b'firewall', '\u9632\u706b\u5899'), (b'storage', '\u5b58\u50a8\u8bbe\u5907'), (b'NLB', 'NetScaler'), (b'wireless', '\u65e0\u7ebfAP'), (b'software', '\u8f6f\u4ef6\u8d44\u4ea7'), (b'others', '\u5176\u5b83\u7c7b')])),
                ('name', models.CharField(max_length=64)),
                ('sn', models.CharField(unique=True, max_length=128, verbose_name='\u8d44\u4ea7SN\u53f7')),
                ('management_ip', models.GenericIPAddressField(null=True, verbose_name='\u7ba1\u7406IP', blank=True)),
                ('trade_date', models.DateField(null=True, verbose_name='\u8d2d\u4e70\u65f6\u95f4', blank=True)),
                ('expire_date', models.DateField(null=True, verbose_name='\u8fc7\u4fdd\u4fee\u671f', blank=True)),
                ('price', models.FloatField(null=True, verbose_name='\u4ef7\u683c', blank=True)),
                ('disk_total', models.FloatField(null=True, verbose_name='\u786c\u76d8\u603b\u91cf(G)', blank=True)),
                ('mem_total', models.FloatField(null=True, verbose_name='\u5185\u5b58\u603b\u91cf(G)', blank=True)),
                ('cabinet_begin', models.IntegerField(null=True, verbose_name='\u5f00\u59cb\u69fd\u4f4d', blank=True)),
                ('cabinet_end', models.IntegerField(null=True, verbose_name='\u7ed3\u675f\u69fd\u4f4d', blank=True)),
                ('status', models.CharField(default=b'start', max_length=64, verbose_name='\u72b6\u6001', choices=[(b'start', '\u5728\u7528'), (b'Disable', '\u505c\u7528\u672a\u4e0b\u67b6'), (b'Disable_down', '\u505c\u7528\u5df2\u4e0b\u67b6'), (b'maintain', '\u7ef4\u4fee')])),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u603b\u8868',
                'verbose_name_plural': '\u8d44\u4ea7\u603b\u8868',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u4e1a\u52a1\u7ebf')),
                ('memo', models.CharField(max_length=64, verbose_name='\u5907\u6ce8', blank=True)),
                ('parent_unit', models.ForeignKey(related_name='parent_level', blank=True, to='asset.BusinessUnit', null=True)),
            ],
            options={
                'verbose_name': '\u4e1a\u52a1\u7ebf',
                'verbose_name_plural': '\u4e1a\u52a1\u7ebf',
            },
        ),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u673a\u67dc\u540d\u79f0')),
                ('memo', models.CharField(max_length=128, null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u673a\u67dc\u8868',
                'verbose_name_plural': '\u673a\u67dc\u8868',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=128, verbose_name='\u5408\u540c\u53f7')),
                ('name', models.CharField(max_length=64, verbose_name='\u5408\u540c\u540d\u79f0')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('price', models.IntegerField(verbose_name='\u5408\u540c\u91d1\u989d')),
                ('detail', models.TextField(null=True, verbose_name='\u5408\u540c\u8be6\u7ec6', blank=True)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('license_num', models.IntegerField(verbose_name='license\u6570\u91cf', blank=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u5408\u540c',
                'verbose_name_plural': '\u5408\u540c',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpu_model', models.CharField(max_length=128, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('cpu_count', models.SmallIntegerField(verbose_name='\u7269\u7406cpu\u4e2a\u6570')),
                ('cpu_core_count', models.SmallIntegerField(verbose_name='cpu\u6838\u6570')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.OneToOneField(to='asset.Asset')),
            ],
            options={
                'verbose_name': 'CPU\u90e8\u4ef6',
                'verbose_name_plural': 'CPU\u90e8\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u69fd\u4f4d')),
                ('manufactory', models.CharField(max_length=64, null=True, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u78c1\u76d8\u578b\u53f7', blank=True)),
                ('capacity', models.FloatField(verbose_name='\u78c1\u76d8\u5bb9\u91cfGB')),
                ('iface_type', models.CharField(default=b'SAS', max_length=64, verbose_name='\u63a5\u53e3\u7c7b\u578b', choices=[(b'SATA', b'SATA'), (b'SAS', b'SAS'), (b'SCSI', b'SCSI'), (b'SSD', b'SSD')])),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.ForeignKey(to='asset.Asset')),
            ],
            options={
                'verbose_name': '\u786c\u76d8',
                'verbose_name_plural': '\u786c\u76d8',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('memo', models.CharField(max_length=128, null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u673a\u623f',
                'verbose_name_plural': '\u673a\u623f',
            },
        ),
        migrations.CreateModel(
            name='Knifebox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u540d\u79f0')),
                ('Intranet_ip', models.GenericIPAddressField(null=True, verbose_name='\u5185\u7f51IP', blank=True)),
                ('Outside_ip', models.GenericIPAddressField(null=True, verbose_name='\u5916\u7f51IP', blank=True)),
                ('memo', models.CharField(max_length=64, null=True, verbose_name='\u5907\u6ce8')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.ForeignKey(to='asset.Asset')),
            ],
            options={
                'verbose_name': '\u5200\u7bb1\u8be6\u60c5',
                'verbose_name_plural': '\u5200\u7bb1\u8be6\u60c5',
            },
        ),
        migrations.CreateModel(
            name='Manufactory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufactory', models.CharField(unique=True, max_length=64, verbose_name='\u5382\u5546\u540d\u79f0')),
                ('support_num', models.CharField(max_length=30, verbose_name='\u652f\u6301\u7535\u8bdd', blank=True)),
                ('memo', models.CharField(max_length=128, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u5382\u5546',
                'verbose_name_plural': '\u5382\u5546',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vlan_ip', models.GenericIPAddressField(null=True, verbose_name='VlanIP', blank=True)),
                ('intranet_ip', models.GenericIPAddressField(null=True, verbose_name='\u5185\u7f51IP', blank=True)),
                ('sn', models.CharField(unique=True, max_length=128, verbose_name='SN\u53f7')),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('port_num', models.SmallIntegerField(null=True, verbose_name='\u7aef\u53e3\u4e2a\u6570', blank=True)),
                ('device_detail', models.TextField(null=True, verbose_name='\u8bbe\u7f6e\u8be6\u7ec6\u914d\u7f6e', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.OneToOneField(to='asset.Asset')),
            ],
            options={
                'verbose_name': '\u7f51\u7edc\u8bbe\u5907',
                'verbose_name_plural': '\u7f51\u7edc\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='\u7f51\u5361\u540d', blank=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u7f51\u5361\u578b\u53f7', blank=True)),
                ('macaddress', models.CharField(unique=True, max_length=64, verbose_name='MAC')),
                ('ipaddress', models.GenericIPAddressField(null=True, verbose_name='IP', blank=True)),
                ('netmask', models.CharField(max_length=64, null=True, blank=True)),
                ('bonding', models.CharField(max_length=64, null=True, blank=True)),
                ('memo', models.CharField(max_length=128, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.ForeignKey(to='asset.Asset')),
            ],
            options={
                'verbose_name': '\u7f51\u5361',
                'verbose_name_plural': '\u7f51\u5361',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'\xe9\x80\x9a\xe7\x9f\xa5\xe5\x86\x85\xe5\xae\xb9')),
                ('status', models.IntegerField(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81')),
                ('create_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u901a\u77e5\u8868',
                'verbose_name_plural': '\u901a\u77e5\u8868',
            },
        ),
        migrations.CreateModel(
            name='RaidAdaptor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u53e3')),
                ('model', models.CharField(max_length=64, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.ForeignKey(to='asset.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('model', models.CharField(max_length=128, verbose_name='\u5185\u5b58\u578b\u53f7')),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u69fd')),
                ('capacity', models.IntegerField(verbose_name='\u5185\u5b58\u5927\u5c0f(MB)')),
                ('memo', models.CharField(max_length=128, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.ForeignKey(to='asset.Asset')),
            ],
            options={
                'verbose_name': 'RAM',
                'verbose_name_plural': 'RAM',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_by', models.CharField(default=b'auto', max_length=32, choices=[(b'auto', b'Auto'), (b'manual', b'Manual')])),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('os_type', models.CharField(max_length=64, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b', blank=True)),
                ('os_distribution', models.CharField(max_length=64, null=True, verbose_name='\u53d1\u578b\u7248\u672c', blank=True)),
                ('os_release', models.CharField(max_length=64, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('asset', models.OneToOneField(to='asset.Asset')),
                ('hosted_on', models.ForeignKey(related_name='hosted_on_server', blank=True, to='asset.Server', null=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name=b'Tag name')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u4e1a\u52a1\u7ebf', blank=True, to='asset.BusinessUnit', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='asset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(verbose_name='\u5408\u540c', blank=True, to='asset.Contract', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(verbose_name='IDC\u673a\u623f', blank=True, to='asset.IDC', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufactory',
            field=models.ForeignKey(verbose_name='\u5236\u9020\u5546', blank=True, to='asset.Manufactory', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(to='asset.Tag', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'slot')]),
        ),
    ]
