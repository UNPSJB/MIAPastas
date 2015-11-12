# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0005_auto_20151111_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='insumo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pedidocliente',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productoterminado',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='receta',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
