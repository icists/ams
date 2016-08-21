# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='accommodation_choice',
            field=models.IntegerField(choices=[(1, b'Triple'), (2, b'Double Twin'), (3, b'Superior Ondol'), (4, b'Deluxe Ondol'), (5, b'No Accommodation')]),
        ),
    ]
