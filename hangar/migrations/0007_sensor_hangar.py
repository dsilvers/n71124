# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0006_auto_20151203_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='hangar',
            field=models.ForeignKey(default=1, to='hangar.Hangar'),
            preserve_default=False,
        ),
    ]
