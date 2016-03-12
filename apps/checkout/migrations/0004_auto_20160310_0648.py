# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_remove_deliverydetails_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverydetails',
            name='price',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deliverydetails',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='deliverydetails',
            name='total',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
