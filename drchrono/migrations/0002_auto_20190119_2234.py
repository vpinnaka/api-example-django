# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-19 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='cell_phone',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='drchrono.Doctor'),
        ),
        migrations.AddField(
            model_name='patient',
            name='state',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='zip_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='drchrono.Doctor'),
        ),
    ]
