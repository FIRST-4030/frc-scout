# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0025_auto_20150214_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='tba_id',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='robot_height',
            field=models.FloatField(null=True, verbose_name='Robot Height'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='team_name',
            field=models.TextField(default=None, null=True, verbose_name='Team Name', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='team_number',
            field=models.IntegerField(verbose_name='Team Number', max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoutdata',
            name='team_website',
            field=models.TextField(default=None, null=True, verbose_name='Team Website', max_length=128),
            preserve_default=True,
        ),
    ]
