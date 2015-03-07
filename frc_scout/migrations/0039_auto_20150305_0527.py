# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0038_auto_20150305_0522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterModelOptions(
            name='matchprivatecomments',
            options={'verbose_name_plural': 'Match private comments'},
        ),
        migrations.AlterModelOptions(
            name='pitscoutdata',
            options={'verbose_name_plural': 'Pit scout data'},
        ),
        migrations.AlterModelOptions(
            name='sitepreferences',
            options={'verbose_name_plural': 'Site preferences'},
        ),
    ]
