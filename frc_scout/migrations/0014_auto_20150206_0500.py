# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0013_auto_20150206_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoutdata',
            name='location',
            field=models.ForeignKey(to='frc_scout.Location', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='team_website',
            field=models.TextField(max_length=128, default=None),
            preserve_default=True,
        ),
    ]
