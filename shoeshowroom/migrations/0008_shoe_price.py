# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeshowroom', '0007_relation_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='price',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
