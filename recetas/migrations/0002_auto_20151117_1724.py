# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chofer',
            name='activo',
            field=models.BooleanField(default=True),
        ),
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
            model_name='cliente',
            name='saldo',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='entregadetalle',
            name='producto_terminado',
            field=models.ForeignKey(blank=True, to='recetas.ProductoTerminado', null=True),
        ),
        migrations.AddField(
            model_name='hojaderuta',
            name='rendida',
            field=models.BooleanField(default=False),
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
            model_name='productosllevadosdetalle',
            name='cantidad_sobrante',
            field=models.PositiveIntegerField(null=True),
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
        migrations.AddField(
            model_name='zona',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='entregadetalle',
            name='pedido_cliente_detalle',
            field=models.ForeignKey(blank=True, to='recetas.PedidoClienteDetalle', null=True),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 17)),
        ),
    ]
