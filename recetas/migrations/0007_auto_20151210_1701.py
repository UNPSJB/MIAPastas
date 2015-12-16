# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0006_auto_20151210_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='numero',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
