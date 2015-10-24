# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151024_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedidoproveedor',
            name='cantidad_insumo',
            field=models.DecimalField(max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='productoterminado',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productoterminado',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Bolsines')]),
        ),
        migrations.AlterField(
            model_name='receta',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Bolsines')]),
        ),
    ]
