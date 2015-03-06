# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0037_auto_20150305_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='tele_shooter_jam',
        ),
        migrations.AddField(
            model_name='match',
            name='tele_container_fell_off',
            field=models.IntegerField(verbose_name='Containers dropped', default=0),
            preserve_default=True,
        ),
    ]
