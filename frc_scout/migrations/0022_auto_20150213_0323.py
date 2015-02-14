# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0021_auto_20150210_0617'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchPrivateComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('match', models.OneToOneField(to='frc_scout.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_foul_context',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='tele_public_comments',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
