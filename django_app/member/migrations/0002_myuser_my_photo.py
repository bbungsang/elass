# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 14:00
from __future__ import unicode_literals

from django.db import migrations
import utils.fields.custom_image_fields


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='my_photo',
            field=utils.fields.custom_image_fields.CustomImageField(blank=True, upload_to='user/%Y/%m/%d'),
        ),
    ]
