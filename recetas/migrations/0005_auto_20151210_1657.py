# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151210_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='numero',
            field=models.PositiveIntegerField(default=2222, unique=True),
        ),
    ]
