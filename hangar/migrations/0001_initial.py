# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('serial', models.CharField(unique=True, max_length=60)),
                ('last_update', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=5, decimal_places=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(to='hangar.Sensor')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='last_data',
            field=models.ForeignKey(related_name='last', to='hangar.SensorData'),
        ),
    ]
