# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jump', '0006_auto_20180108_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jump_Notice',
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
    ]
