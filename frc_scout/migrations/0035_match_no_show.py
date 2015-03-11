# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0034_auto_20150304_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='no_show',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
