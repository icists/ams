# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import icists.apps.session.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField()),
                ('nationality', models.CharField(max_length=45)),
                ('gender', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45)),
                ('major', models.CharField(max_length=45)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=b'profilepicture', validators=[icists.apps.session.models.validate_image])),
                ('how_you_found_us', models.CharField(max_length=100, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('university', models.ForeignKey(to='session.University')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
