# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangar', '0008_auto_20151216_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='powerschedule',
            name='comment',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
