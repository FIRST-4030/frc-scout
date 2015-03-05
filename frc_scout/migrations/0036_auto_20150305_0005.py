# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0035_match_no_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='auto_start_x',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_start_y',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=8),
            preserve_default=True,
        ),
    ]
