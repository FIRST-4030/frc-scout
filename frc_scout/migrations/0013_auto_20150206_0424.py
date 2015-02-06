# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0012_pitscoutdata_has_strafing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitscoutdata',
            name='team_name',
            field=models.TextField(max_length=64, default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='tote_stack_capacity',
            field=models.IntegerField(max_length=3, default=None),
            preserve_default=True,
        ),
    ]
