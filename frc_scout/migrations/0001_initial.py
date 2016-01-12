# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import frc_scout.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerStack',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('height', models.IntegerField(default=1)),
                ('containers_added', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('tba_event_code', models.TextField(blank=True, null=True)),
                ('venue_address', models.TextField(null=True)),
                ('location', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('scout_team_number', models.IntegerField(max_length=5)),
                ('scout_name', models.TextField()),
                ('no_show', models.BooleanField(default=False)),
                ('team_number', models.IntegerField(max_length=5)),
                ('match_number', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=frc_scout.models.get_current_time)),
                ('auto_start_x', models.DecimalField(default=0, max_digits=20, decimal_places=16)),
                ('auto_start_y', models.DecimalField(default=0, max_digits=20, decimal_places=16)),
                ('auto_yellow_stacked_totes', models.IntegerField(default=0, verbose_name='Yellow totes stacked')),
                ('auto_yellow_moved_totes', models.IntegerField(default=0, verbose_name='Yellow totes moved')),
                ('auto_grey_acquired_totes', models.IntegerField(default=0, verbose_name='Grey totes acquired')),
                ('auto_step_center_acquired_containers', models.IntegerField(default=0, verbose_name='Containers acquired from center step')),
                ('auto_ground_acquired_containers', models.IntegerField(default=0, verbose_name='Containers acquired from ground')),
                ('auto_moved_containers', models.IntegerField(default=0, verbose_name='Containers moved')),
                ('auto_moved_to_auto_zone', models.BooleanField(default=False, verbose_name='Moved to Auto Zone')),
                ('auto_no_auto', models.BooleanField(default=False, verbose_name='No autonomous')),
                ('auto_fouls', models.IntegerField(default=0, verbose_name='Autonomous mess-ups committed')),
                ('auto_interference', models.IntegerField(default=0, verbose_name='Interference committed')),
                ('tele_picked_up_ground_upright_totes', models.IntegerField(default=0, verbose_name='Upright totes picked up')),
                ('tele_picked_up_upside_down_totes', models.IntegerField(default=0, verbose_name='Upside-down totes picked up')),
                ('tele_picked_up_sideways_totes', models.IntegerField(default=0, verbose_name='Sideways totes picked up')),
                ('tele_picked_up_human_station_totes', models.IntegerField(default=0, verbose_name='Totes received from human station')),
                ('tele_picked_up_sideways_containers', models.IntegerField(default=0, verbose_name='Sideways containers picked up')),
                ('tele_picked_up_upright_containers', models.IntegerField(default=0, verbose_name='Upright containers picked up')),
                ('tele_picked_up_center_step_containers', models.IntegerField(default=0, verbose_name='Center-step containers picked up')),
                ('tele_pushed_litter', models.IntegerField(default=0, verbose_name='Litter pushed')),
                ('tele_placed_in_container_litter', models.IntegerField(default=0, verbose_name='Litter placed in container')),
                ('tele_fouls', models.IntegerField(default=0, verbose_name='Teleoperated fouls committed')),
                ('tele_knocked_over_stacks', models.IntegerField(default=0, verbose_name='Stacks knocked over')),
                ('tele_dead_bot', models.BooleanField(default=False, verbose_name='Robot died')),
                ('tele_container_fell_off', models.IntegerField(default=0, verbose_name='Containers dropped')),
                ('tele_foul_context', models.TextField(blank=True, null=True)),
                ('tele_public_comments', models.TextField(blank=True, null=True)),
                ('match_final_score', models.IntegerField(verbose_name='Final match score', null=True)),
                ('location', models.ForeignKey(to='frc_scout.Location')),
                ('scout', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchPrivateComments',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('match', models.OneToOneField(to='frc_scout.Match')),
            ],
            options={
                'verbose_name_plural': 'Match private comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PitScoutData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('pitscout_name', models.TextField(blank=True, null=True)),
                ('pitscout_team_number', models.IntegerField(blank=True, null=True)),
                ('team_number', models.IntegerField(verbose_name='Team Number', max_length=5)),
                ('team_name', models.TextField(default=None, verbose_name='Team Name', max_length=64, null=True)),
                ('team_website', models.TextField(default=None, verbose_name='Team Website', max_length=128, null=True)),
                ('robot_height', models.FloatField(verbose_name='Robot Height', null=True)),
                ('robot_weight', models.FloatField(null=True)),
                ('robot_speed', models.FloatField(null=True)),
                ('driver_1', models.TextField(default=None, max_length=64, null=True)),
                ('driver_2', models.TextField(default=None, max_length=64, null=True)),
                ('coach', models.TextField(default=None, max_length=64, null=True)),
                ('drive_coach_is_mentor', models.NullBooleanField()),
                ('can_move_totes', models.NullBooleanField()),
                ('can_move_containers', models.NullBooleanField()),
                ('can_acquire_containers', models.NullBooleanField()),
                ('auto_start_x', models.FloatField(null=True)),
                ('auto_start_y', models.FloatField(null=True)),
                ('tote_stack_capacity', models.IntegerField(default=None, max_length=3, null=True)),
                ('human_tote_loading', models.NullBooleanField()),
                ('human_litter_loading', models.NullBooleanField()),
                ('human_litter_throwing', models.NullBooleanField()),
                ('has_turret', models.NullBooleanField()),
                ('has_strafing', models.NullBooleanField()),
                ('known_strengths', models.TextField(max_length=256, null=True)),
                ('known_weaknesses', models.TextField(max_length=256, null=True)),
                ('image_id', models.TextField(blank=True, max_length=256, null=True)),
                ('image_link', models.TextField(blank=True, max_length=256, null=True)),
                ('image_type', models.TextField(blank=True, max_length=64, null=True)),
                ('location', models.ForeignKey(to='frc_scout.Location')),
                ('scout', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pit scout data',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SitePreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('site_url', models.TextField()),
                ('login_message', models.TextField(blank=True, null=True)),
                ('home_message', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Site preferences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('team_number', models.IntegerField(max_length=5)),
                ('team_name', models.TextField(blank=True, max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ToteStack',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('start_height', models.IntegerField(default=0)),
                ('totes_added', models.IntegerField(default=0)),
                ('x', models.DecimalField(decimal_places=16, max_digits=20)),
                ('y', models.DecimalField(decimal_places=16, max_digits=20)),
                ('coop_stack', models.BooleanField(default=False)),
                ('match', models.ForeignKey(to='frc_scout.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('team_manager', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('team', models.ForeignKey(to='frc_scout.Team', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='containerstack',
            name='match',
            field=models.ForeignKey(to='frc_scout.Match'),
            preserve_default=True,
        ),
    ]
