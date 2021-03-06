# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-13 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_dailymetrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailymetrics',
            name='pa_count30to45',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dailymetrics',
            name='pa_count60to65',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dailymetrics',
            name='pa_invvalue',
            field=models.FloatField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dailymetrics',
            name='sv_old_ro_count',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dailymetrics',
            name='sv_ro_count',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]
