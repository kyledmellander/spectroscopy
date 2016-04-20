# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='id',
        ),
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='signup',
            name='lastName',
            field=models.CharField(max_length=120),
        ),
    ]
