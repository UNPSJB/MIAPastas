# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0015_auto_20151009_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='stock',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
    ]
