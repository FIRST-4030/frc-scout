# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0014_auto_20150206_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitscoutdata',
            name='can_acquire_containers',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='can_move_containers',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='can_move_totes',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='has_strafing',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='has_turret',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='human_litter_loading',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='human_tote_loading',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='team_name',
            field=models.TextField(default=None, max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='team_website',
            field=models.TextField(default=None, max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='tote_stack_capacity',
            field=models.IntegerField(default=None, max_length=3, null=True),
            preserve_default=True,
        ),
    ]
