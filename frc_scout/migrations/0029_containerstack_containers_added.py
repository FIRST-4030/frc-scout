# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0028_auto_20150214_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='containerstack',
            name='containers_added',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
