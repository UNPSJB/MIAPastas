# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cuit',
            field=models.CharField(unique=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 12, 13)),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='cuit',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
