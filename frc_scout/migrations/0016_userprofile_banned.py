# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0015_auto_20150206_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='banned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
