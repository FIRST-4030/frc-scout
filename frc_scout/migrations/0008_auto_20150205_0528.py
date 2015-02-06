# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0007_auto_20150205_0346'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerStack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('height', models.IntegerField(default=1)),
                ('match', models.ForeignKey(to='frc_scout.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='binstack',
            name='match',
        ),
        migrations.DeleteModel(
            name='BinStack',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='auto_ground_acquired_bins',
            new_name='auto_ground_acquired_containers',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='auto_moved_bins',
            new_name='auto_moved_containers',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='auto_step_center_acquired_bins',
            new_name='auto_step_center_acquired_containers',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tele_picked_up_center_step_bins',
            new_name='tele_picked_up_center_step_containers',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tele_picked_up_sideways_bins',
            new_name='tele_picked_up_sideways_containers',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tele_picked_up_upright_bins',
            new_name='tele_picked_up_upright_containers',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tele_placed_in_bin_litter',
            new_name='tele_placed_in_container_litter',
        ),
    ]
