# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0033_auto_20150225_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='tele_foul_context',
            new_name='mess_up_context',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tele_fouls',
            new_name='tele_mess_ups',
        ),
        migrations.RemoveField(
            model_name='match',
            name='auto_fouls',
        ),
        migrations.AddField(
            model_name='match',
            name='auto_mess_ups',
            field=models.IntegerField(default=0, verbose_name='Autonomous mess-ups committed'),
            preserve_default=True,
        ),
    ]
