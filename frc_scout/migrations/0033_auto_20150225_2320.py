# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0032_auto_20150224_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoutdata',
            name='pitscout_name',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='pitscout_team_number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
