# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-21 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0006_auto_20190121_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='complete_time',
            field=models.DateTimeField(null=True),
        ),
    ]
