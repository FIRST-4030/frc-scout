# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frc_scout', '0022_auto_20150213_0323'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('site_url', models.TextField()),
                ('login_message', models.TextField(blank=True, null=True)),
                ('home_message', models.TextField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
