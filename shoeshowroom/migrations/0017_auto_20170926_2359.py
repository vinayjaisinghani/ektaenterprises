# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeshowroom', '0016_auto_20170926_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='floater',
            field=models.CharField(choices=[(b'shoe_boot', b'shoe_boot'), (b'shoe_oxford', b'shoe_oxford'), (b'shoe_loafer', b'shoe_loafer'), (b'shoe_sneaker', b'shoe_sneaker'), (b'shoe_sport', b'shoe_sport'), (b'shoe_boot', b'shoe_boot'), (b'slipper_beach', b'slipper_beach'), (b'slipper_glider', b'slipper_glider'), (b'slipper_printed', b'slipper_printed'), (b'sandal_mules', b'sandal_mules'), (b'sandal_glider', b'sandal_glider'), (b'sandal_opentoe', b'sandal_opentoe'), (b'sandal_closetoe', b'sandal_closetoe')], max_length=200),
        ),
    ]
