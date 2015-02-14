# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0008_auto_20150205_0528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='tele_misc_comments',
            new_name='tele_public_comments',
        ),
    ]
