# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0002_auto_20151112_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='last_data',
            field=models.ForeignKey(related_name='last', to='hangar.SensorData', null=True),
        ),
    ]
