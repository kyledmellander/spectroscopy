# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 01:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0001_initial'),
    ]

    operations = [
        migrations.RenameField("Sample", "sample_type","mineral_type"),
    ]
