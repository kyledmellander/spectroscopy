# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0013_auto_20170627_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='flagged',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]