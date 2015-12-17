# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0002_auto_20151217_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='breakfast_krw',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='breakfast_usd',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='posttour_krw',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='posttour_usd',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='pretour_krw',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='pretour_usd',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
