# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0004_auto_20170116_0205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sampletype',
            options={'verbose_name': 'Sample Type', 'verbose_name_plural': 'Sample Types'},
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='typeOfSample',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name=b'Type Of Sample'),
        ),
    ]
