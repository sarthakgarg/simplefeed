# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplefeed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='target',
            old_name='target_url',
            new_name='url',
        ),
        migrations.AddField(
            model_name='target',
            name='content',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
