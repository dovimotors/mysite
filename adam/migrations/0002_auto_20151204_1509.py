# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adamfiles',
            name='DBFPath',
            field=models.FilePathField(path=b'f:\\adamexports\\adamcache\\', recursive=True),
        ),
    ]
