# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentlogin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.FileField(null=True, upload_to='image/'),
        ),
    ]