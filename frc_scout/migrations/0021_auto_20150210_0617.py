# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0020_auto_20150210_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='message',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
