# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-07 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mars', '0008_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('position', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Team Member',
                'verbose_name_plural': 'Team Members',
            },
        ),
        migrations.AlterModelOptions(
            name='database',
            options={'ordering': ['position', 'name']},
        ),
        migrations.AddField(
            model_name='database',
            name='position',
            field=models.IntegerField(default=1),
        ),
    ]
