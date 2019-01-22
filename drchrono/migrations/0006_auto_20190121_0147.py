# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-21 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0005_appointment_waittime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='waittime',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='reason',
            field=models.CharField(max_length=200, null=True),
        ),
    ]