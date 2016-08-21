# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_stage', models.CharField(default=b'BE', max_length=2, choices=[(b'BE', b'Before Early'), (b'E', b'Early'), (b'EC', b'Early Closed'), (b'R', b'Regular'), (b'RC', b'Regular Closed'), (b'L', b'Late'), (b'LC', b'Late Closed')])),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('early_price_krw', models.IntegerField()),
                ('early_price_usd', models.IntegerField()),
                ('regular_price_krw', models.IntegerField()),
                ('regular_price_usd', models.IntegerField()),
                ('late_price_krw', models.IntegerField()),
                ('late_price_usd', models.IntegerField()),
                ('group_dc_USD', models.IntegerField()),
                ('group_dc_KRW', models.IntegerField()),
            ],
        ),
    ]
