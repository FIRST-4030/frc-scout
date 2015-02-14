# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0005_auto_20150131_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='team',
            field=models.IntegerField(max_length=5),
            preserve_default=True,
        ),
    ]
