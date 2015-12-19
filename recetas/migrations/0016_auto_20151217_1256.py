# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 12, 17)),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='direccion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='localidad',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombre_dueno',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='provincia',
            field=models.CharField(max_length=50),
        ),
    ]
