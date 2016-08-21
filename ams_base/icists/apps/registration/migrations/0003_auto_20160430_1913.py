# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150818_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='project_topic_2nd',
            field=models.ForeignKey(related_name='application_project_2nd', blank=True, to='registration.ProjectTopic'),
        ),
    ]
