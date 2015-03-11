# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0019_userprofile_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='position',
            new_name='message',
        ),
    ]
