# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0023_sitepreferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='auto_fouls',
            field=models.IntegerField(default=0, verbose_name='Autonomous fouls committed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_grey_acquired_totes',
            field=models.IntegerField(default=0, verbose_name='Grey totes acquired'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_ground_acquired_containers',
            field=models.IntegerField(default=0, verbose_name='Containers acquired from ground'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_interference',
            field=models.IntegerField(default=0, verbose_name='Interference committed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_moved_containers',
            field=models.IntegerField(default=0, verbose_name='Containers moved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_moved_to_auto_zone',
            field=models.BooleanField(default=False, verbose_name='Moved to Auto Zone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_no_auto',
            field=models.BooleanField(default=False, verbose_name='No autonomous'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_step_center_acquired_containers',
            field=models.IntegerField(default=0, verbose_name='Containers acquired from center step'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_yellow_moved_totes',
            field=models.IntegerField(default=0, verbose_name='Yellow totes moved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='auto_yellow_stacked_totes',
            field=models.IntegerField(default=0, verbose_name='Yellow totes stacked'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_dead_bot',
            field=models.BooleanField(default=False, verbose_name='Robot died'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_fouls',
            field=models.IntegerField(default=0, verbose_name='Teleoperated fouls committed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_knocked_over_stacks',
            field=models.IntegerField(default=0, verbose_name='Stacks knocked over'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_center_step_containers',
            field=models.IntegerField(default=0, verbose_name='Center-step containers picked up'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_ground_upright_totes',
            field=models.IntegerField(default=0, verbose_name='Upright totes picked up'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_human_station_totes',
            field=models.IntegerField(default=0, verbose_name='Totes received from human station'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_sideways_containers',
            field=models.IntegerField(default=0, verbose_name='Sideways containers picked up'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_sideways_totes',
            field=models.IntegerField(default=0, verbose_name='Sideways totes picked up'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_upright_containers',
            field=models.IntegerField(default=0, verbose_name='Upright containers picked up'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_picked_up_upside_down_totes',
            field=models.IntegerField(default=0, verbose_name='Upside-down totes picked up'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_placed_in_container_litter',
            field=models.IntegerField(default=0, verbose_name='Litter placed in container'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_pushed_litter',
            field=models.IntegerField(default=0, verbose_name='Litter pushed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_shooter_jam',
            field=models.BooleanField(default=False, verbose_name='Shooter jammed'),
            preserve_default=True,
        ),
    ]
