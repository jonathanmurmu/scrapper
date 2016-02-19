# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0002_auto_20160212_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='city',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='state',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
