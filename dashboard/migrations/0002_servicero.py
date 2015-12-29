# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRO',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statdate', models.DateField(auto_now=True)),
                ('totalrocount', models.IntegerField()),
                ('oldrocount', models.IntegerField()),
                ('printedrocount', models.IntegerField()),
                ('printedro_custpay', models.FloatField()),
                ('printedro_intpay', models.FloatField()),
                ('printedro_warpay', models.FloatField()),
                ('printedro_extpay', models.FloatField()),
            ],
        ),
    ]
