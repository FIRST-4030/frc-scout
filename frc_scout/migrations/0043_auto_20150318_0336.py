# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0042_pitscoutdata_drive_coach_is_mentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='venue_address',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
