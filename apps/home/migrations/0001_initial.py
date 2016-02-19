# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
                ('product_type', models.CharField(blank=True, null=True, max_length=30)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('landing_url', models.URLField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('description', models.CharField(blank=True, null=True, max_length=255)),
                ('scraped_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
