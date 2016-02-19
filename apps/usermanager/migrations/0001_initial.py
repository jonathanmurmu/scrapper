# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.usermanager.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('marital', models.CharField(max_length=1, choices=[(1, 'Single'), (2, 'Married')], null=True, blank=True)),
                ('gender', models.CharField(max_length=1, choices=[(1, 'Male'), (2, 'Female')], null=True, blank=True)),
                ('address', models.CharField(max_length=254, null=True, blank=True)),
                ('street', models.CharField(max_length=30, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=6, null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
                ('extra_note', models.CharField(max_length=254, null=True, blank=True)),
                ('mail', models.BooleanField(max_length=1)),
                ('message', models.BooleanField(max_length=1)),
                ('phonecall', models.BooleanField(max_length=1)),
                ('other', models.BooleanField(max_length=1)),
                ('image', models.ImageField(null=True, upload_to=apps.usermanager.models.generate_filename, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
