# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='group_dc_KRW',
            new_name='group_dc_krw',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='group_dc_USD',
            new_name='group_dc_usd',
        ),
    ]
