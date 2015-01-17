# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='team',
            field=models.ForeignKey(null=True, to='frc_scout.Team'),
            preserve_default=True,
        ),
    ]
