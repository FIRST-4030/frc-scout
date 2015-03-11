# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0031_auto_20150218_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoutdata',
            name='image_id',
            field=models.TextField(blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='image_link',
            field=models.TextField(blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoutdata',
            name='image_type',
            field=models.TextField(blank=True, null=True, max_length=64),
            preserve_default=True,
        ),
    ]
