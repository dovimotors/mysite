# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_servicero'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicero',
            old_name='printedro_custpay',
            new_name='ro_custpay',
        ),
        migrations.RenameField(
            model_name='servicero',
            old_name='printedro_extpay',
            new_name='ro_extpay',
        ),
        migrations.RenameField(
            model_name='servicero',
            old_name='printedro_intpay',
            new_name='ro_intpay',
        ),
        migrations.RenameField(
            model_name='servicero',
            old_name='printedro_warpay',
            new_name='ro_warpay',
        ),
    ]
