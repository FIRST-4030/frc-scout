# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0027_auto_20150214_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='scout_name',
            field=models.TextField(default='Unknown'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='scout_team_number',
            field=models.IntegerField(default=0, max_length=5),
            preserve_default=False,
        ),
    ]
