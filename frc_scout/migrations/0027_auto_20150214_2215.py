# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0026_auto_20150214_2142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='tba_id',
            new_name='tba_event_code',
        ),
    ]
