# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0004_auto_20150124_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totestack',
            name='end_height',
        ),
        migrations.AddField(
            model_name='totestack',
            name='totes_added',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
