# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0014_auto_20151005_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='stock',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
