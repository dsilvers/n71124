# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0005_auto_20151112_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hangar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('api_key', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PowerSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PowerSwitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial', models.CharField(unique=True, max_length=60)),
                ('hangar', models.ForeignKey(to='hangar.Hangar')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='unit',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='powerschedule',
            name='switch',
            field=models.ForeignKey(to='hangar.PowerSwitch'),
        ),
    ]
