# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0007_sensor_hangar'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerManualControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('expiration', models.DateTimeField()),
                ('status', models.BooleanField()),
                ('switch', models.ForeignKey(to='hangar.PowerSwitch')),
            ],
        ),
        migrations.AddField(
            model_name='powerschedule',
            name='departure',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
