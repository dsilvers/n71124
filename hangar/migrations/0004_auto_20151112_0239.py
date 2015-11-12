# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0003_auto_20151112_0237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='last_data',
        ),
        migrations.AddField(
            model_name='sensor',
            name='last_value',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
    ]
