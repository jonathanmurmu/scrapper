# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0007_auto_20160222_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivation',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
