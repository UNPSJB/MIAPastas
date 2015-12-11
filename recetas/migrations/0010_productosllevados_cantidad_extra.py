# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0009_auto_20151216_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosllevados',
            name='cantidad_extra',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
