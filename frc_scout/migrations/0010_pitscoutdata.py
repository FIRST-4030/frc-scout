# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frc_scout', '0009_auto_20150205_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='PitScoutData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('team_number', models.IntegerField(max_length=5)),
                ('team_name', models.TextField(max_length=64)),
                ('can_move_totes', models.BooleanField()),
                ('can_move_containers', models.BooleanField()),
                ('can_acquire_containers', models.BooleanField()),
                ('tote_stack_capacity', models.IntegerField(max_length=3)),
                ('human_tote_loading', models.BooleanField()),
                ('human_litter_loading', models.BooleanField()),
                ('has_turret', models.BooleanField()),
                ('scout', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
