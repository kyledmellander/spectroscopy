# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-07 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0005_auto_20170116_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
