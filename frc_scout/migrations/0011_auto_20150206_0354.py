# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0010_pitscoutdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitscoutdata',
            name='can_acquire_containers',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='can_move_containers',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='can_move_totes',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='has_turret',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='human_litter_loading',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='human_tote_loading',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
    ]
