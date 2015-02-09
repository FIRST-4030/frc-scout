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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('height', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('team_number', models.IntegerField(max_length=5)),
                ('match_number', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=frc_scout.models.get_current_time)),
                ('auto_start_x', models.DecimalField(max_digits=8, decimal_places=8)),
                ('auto_start_y', models.DecimalField(max_digits=8, decimal_places=8)),
                ('auto_yellow_stacked_totes', models.IntegerField(default=0)),
                ('auto_yellow_moved_totes', models.IntegerField(default=0)),
                ('auto_grey_acquired_totes', models.IntegerField(default=0)),
                ('auto_step_center_acquired_containers', models.IntegerField(default=0)),
                ('auto_ground_acquired_containers', models.IntegerField(default=0)),
                ('auto_moved_containers', models.IntegerField(default=0)),
                ('auto_moved_to_auto_zone', models.BooleanField(default=False)),
                ('auto_no_auto', models.BooleanField(default=False)),
                ('auto_fouls', models.IntegerField(default=0)),
                ('auto_interference', models.IntegerField(default=0)),
                ('tele_picked_up_ground_upright_totes', models.IntegerField(default=0)),
                ('tele_picked_up_upside_down_totes', models.IntegerField(default=0)),
                ('tele_picked_up_sideways_totes', models.IntegerField(default=0)),
                ('tele_picked_up_human_station_totes', models.IntegerField(default=0)),
                ('tele_picked_up_sideways_containers', models.IntegerField(default=0)),
                ('tele_picked_up_upright_containers', models.IntegerField(default=0)),
                ('tele_picked_up_center_step_containers', models.IntegerField(default=0)),
                ('tele_pushed_litter', models.IntegerField(default=0)),
                ('tele_placed_in_container_litter', models.IntegerField(default=0)),
                ('tele_fouls', models.IntegerField(default=0)),
                ('tele_knocked_over_stacks', models.IntegerField(default=0)),
                ('tele_dead_bot', models.BooleanField(default=False)),
                ('tele_shooter_jam', models.BooleanField(default=False)),
                ('tele_foul_context', models.TextField()),
                ('tele_public_comments', models.TextField()),
                ('location', models.ForeignKey(to='frc_scout.Location')),
                ('scout', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('team_number', models.IntegerField(max_length=5)),
                ('team_name', models.TextField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ToteStack',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('start_height', models.IntegerField(default=0)),
                ('totes_added', models.IntegerField(default=0)),
                ('x', models.DecimalField(max_digits=8, decimal_places=8)),
                ('y', models.DecimalField(max_digits=8, decimal_places=8)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('team_manager', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
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
