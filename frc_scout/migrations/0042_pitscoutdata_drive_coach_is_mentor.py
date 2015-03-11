# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0041_auto_20150305_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoutdata',
            name='drive_coach_is_mentor',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
