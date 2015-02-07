# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0017_remove_userprofile_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoutdata',
            name='auto_start_x',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='auto_start_y',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='coach',
            field=models.TextField(default=None, null=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='driver_1',
            field=models.TextField(default=None, null=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='driver_2',
            field=models.TextField(default=None, null=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='human_litter_throwing',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='known_strengths',
            field=models.TextField(null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='known_weaknesses',
            field=models.TextField(null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='robot_height',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='robot_speed',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='robot_weight',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
