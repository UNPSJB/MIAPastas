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
        migrations.AddField(
            model_name='cliente',
            name='saldo',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='entregadetalle',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado', null=True),
        ),
        migrations.AddField(
            model_name='productosllevadosdetalle',
            name='cantidad_sobrante',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='factura',
            field=models.ForeignKey(to='recetas.Factura', null=True),
        ),
        migrations.AlterField(
            model_name='entregadetalle',
            name='pedido_cliente_detalle',
            field=models.ForeignKey(to='recetas.PedidoClienteDetalle', null=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='monto_pagado',
            field=models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 14)),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='monto_pagado',
            field=models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
    ]
