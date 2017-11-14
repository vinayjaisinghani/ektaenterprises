# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeshowroom', '0015_relation_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('myid', models.AutoField(primary_key=True, serialize=False)),
                ('floater', models.CharField(choices=[(b'shoe', b'shoe'), (b'slipper', b'slipper'), (b'sandal', b'sandal')], max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('modelname', models.CharField(max_length=200)),
                ('price', models.PositiveIntegerField(null=True)),
                ('img1', models.ImageField(blank=True, null=True, upload_to=b'media/')),
                ('img2', models.ImageField(blank=True, null=True, upload_to=b'media/')),
                ('img3', models.ImageField(blank=True, null=True, upload_to=b'media/')),
                ('image_height', models.PositiveIntegerField(blank=True, default=b'100', editable=False, null=True)),
                ('image_width', models.PositiveIntegerField(blank=True, default=b'100', editable=False, null=True)),
                ('category', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female'), (b'K', b'Kids')], max_length=1)),
                ('size6', models.PositiveIntegerField(choices=[(1, b'Available'), (0, b'Unavailable')], default=0)),
                ('size7', models.PositiveIntegerField(choices=[(1, b'Available'), (0, b'Unavailable')], default=0)),
                ('size8', models.PositiveIntegerField(choices=[(1, b'Available'), (0, b'Unavailable')], default=0)),
                ('size9', models.PositiveIntegerField(choices=[(1, b'Available'), (0, b'Unavailable')], default=0)),
                ('size10', models.PositiveIntegerField(choices=[(1, b'Available'), (0, b'Unavailable')], default=0)),
                ('outer_material', models.CharField(max_length=200, null=True)),
                ('occasion', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('pack_of', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.DeleteModel(
            name='shoe',
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='shoeid',
            new_name='productid',
        ),
    ]
