# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_product_site_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug_name',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
