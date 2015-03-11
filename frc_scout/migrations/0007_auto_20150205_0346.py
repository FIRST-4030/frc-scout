# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0006_auto_20150205_0338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='team',
            new_name='team_number',
        ),
    ]
