# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-07 06:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0006_database'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sample',
            options={'verbose_name': 'Sample', 'verbose_name_plural': 'Samples'},
        ),
    ]
