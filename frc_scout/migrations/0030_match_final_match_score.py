# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0029_containerstack_containers_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='final_match_score',
            field=models.IntegerField(null=True, verbose_name='Final match score'),
            preserve_default=True,
        ),
    ]
