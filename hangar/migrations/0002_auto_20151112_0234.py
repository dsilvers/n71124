# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='last_data',
            field=models.ForeignKey(related_name='last', blank=True, to='hangar.SensorData', null=True),
        ),
    ]
