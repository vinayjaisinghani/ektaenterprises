# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeshowroom', '0022_auto_20170927_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='querysub',
            name='answer',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
