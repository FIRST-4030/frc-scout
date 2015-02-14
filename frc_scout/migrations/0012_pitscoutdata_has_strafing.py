# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0011_auto_20150206_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoutdata',
            name='has_strafing',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
    ]
