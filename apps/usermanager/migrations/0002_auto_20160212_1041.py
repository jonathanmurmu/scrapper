# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='mail',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='message',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='other',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='phonecall',
            field=models.BooleanField(default=False),
        ),
    ]
