# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudad',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='receta',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='zona',
            name='activo',
        ),
        migrations.AddField(
            model_name='chofer',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productosllevados',
            name='precio',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 20)),
        ),
    ]
