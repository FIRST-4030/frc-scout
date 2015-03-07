# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0030_match_final_match_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='final_match_score',
            new_name='match_final_score',
        ),
    ]
