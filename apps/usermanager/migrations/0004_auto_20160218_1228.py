# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0003_auto_20160212_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='gender',
            field=models.CharField(blank=True, null=True, choices=[('1', 'Male'), ('2', 'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/uploads/'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='marital',
            field=models.CharField(blank=True, null=True, choices=[('1', 'Single'), ('2', 'Married')], max_length=1),
        ),
    ]
