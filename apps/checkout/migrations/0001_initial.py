# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_product_site_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order_id', models.CharField(max_length=20, blank=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('address', models.CharField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('city', models.CharField(max_length=20, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=10, null=True, blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(to='home.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
