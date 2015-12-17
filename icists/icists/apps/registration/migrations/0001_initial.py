# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hotel_name', models.CharField(max_length=45)),
                ('hotel_room', models.CharField(max_length=45)),
                ('accommodation_payment', models.IntegerField()),
                ('gender', models.CharField(max_length=45)),
                ('availability', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_category', models.CharField(default=b'R', max_length=1, choices=[(b'E', b'Early'), (b'R', b'Regular'), (b'L', b'Late')])),
                ('screening_result', models.CharField(default=b'P', max_length=1, choices=[(b'A', b'Accepted'), (b'D', b'Dismissed'), (b'P', b'Pending')])),
                ('results_embargo', models.BooleanField(default=True)),
                ('essay_text', models.TextField()),
                ('visa_letter_required', models.CharField(default=b'N', max_length=1, choices=[(b'Y', b'Yes'), (b'N', b'No')])),
                ('financial_aid', models.CharField(default=b'N', max_length=1, choices=[(b'Y', b'Yes'), (b'N', b'No')])),
                ('group_name', models.CharField(max_length=45, blank=True)),
                ('group_discount', models.BooleanField(default=False)),
                ('previously_participated', models.CharField(default=b'N', max_length=1, choices=[(b'Y', b'Yes'), (b'N', b'No')])),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
                ('submit_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EssayTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('number', models.IntegerField()),
                ('text', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accommodation_choice', models.IntegerField(choices=[(1, b'Standard Ondol'), (2, b'Standard Ondol Twin'), (3, b'Deluxe Ondol'), (4, b'Suite Ondol'), (5, b'KAIST Dormitory'), (6, b'No Accommodation')])),
                ('is_accommodation_assigned', models.BooleanField(default=False)),
                ('project_team_no', models.PositiveSmallIntegerField()),
                ('payment_status', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'Not Paid'), (b'P', b'Paid'), (b'L', b'Less Paid'), (b'O', b'Over Paid')])),
                ('payment_option', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Paypal'), (b'B', b'Bank Transfer')])),
                ('required_payment_krw', models.IntegerField()),
                ('required_payment_usd', models.IntegerField()),
                ('remitter_name', models.CharField(max_length=45, null=True, blank=True)),
                ('breakfast_option', models.BooleanField(default=False)),
                ('dietary_option', models.CharField(max_length=45, null=True, blank=True)),
                ('pretour', models.BooleanField(default=False)),
                ('posttour', models.BooleanField(default=False)),
                ('group_discount', models.BooleanField(default=False)),
                ('submit_time', models.DateTimeField(null=True)),
                ('accommodation', models.ForeignKey(related_name='participant', to='registration.Accommodation', null=True)),
                ('application', models.OneToOneField(related_name='participant', to='registration.Application')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('number', models.IntegerField()),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('q1', models.TextField(default=b'', null=True, blank=True)),
                ('q2', models.TextField(default=b'', null=True, blank=True)),
                ('q3', models.TextField(default=b'', null=True, blank=True)),
                ('q4', models.TextField(default=b'', null=True, blank=True)),
                ('application', models.ForeignKey(related_name='survey', to='registration.Application')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='essay_topic',
            field=models.ForeignKey(related_name='application_essay', to='registration.EssayTopic'),
        ),
        migrations.AddField(
            model_name='application',
            name='project_topic',
            field=models.ForeignKey(related_name='application_project', to='registration.ProjectTopic'),
        ),
        migrations.AddField(
            model_name='application',
            name='project_topic_2nd',
            field=models.ForeignKey(related_name='application_project_2nd', to='registration.ProjectTopic'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(related_name='application', to=settings.AUTH_USER_MODEL),
        ),
    ]
