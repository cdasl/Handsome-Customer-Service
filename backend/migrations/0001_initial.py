# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('CID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('EID', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=120)),
                ('name', models.CharField(max_length=10)),
                ('state', models.IntegerField(default=0)),
                ('service_number', models.IntegerField(default=0)),
                ('serviced_number', models.IntegerField(default=0)),
                ('last_login', models.DateField()),
                ('salt', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('DID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('EID', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('end_time', models.DateTimeField(verbose_name='end time')),
                ('UID', models.CharField(max_length=50)),
                ('CID', models.CharField(max_length=50)),
                ('feedback', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('EID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('robot_icon', models.CharField(max_length=50)),
                ('robot_name', models.CharField(max_length=10)),
                ('state', models.IntegerField(default=0)),
                ('salt', models.CharField(max_length=8)),
                ('chatbox_type', models.IntegerField(default=1)),
                ('robot_state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('MID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('SID', models.CharField(max_length=50)),
                ('RID', models.CharField(max_length=50)),
                ('DID', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(verbose_name='message time')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('QID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('EID', models.CharField(max_length=50)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('category', models.CharField(default='unclassified', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('UID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('info', models.CharField(max_length=100)),
            ],
        ),
    ]
