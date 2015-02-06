# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0016_userprofile_banned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='banned',
        ),
    ]
