# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeshowroom', '0009_shoe_img2'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to=b'media/'),
        ),
    ]