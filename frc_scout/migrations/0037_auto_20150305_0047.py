# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0036_auto_20150305_0005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='auto_mess_ups',
            new_name='auto_fouls',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='mess_up_context',
            new_name='tele_foul_context',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tele_mess_ups',
            new_name='tele_fouls',
        ),
    ]
