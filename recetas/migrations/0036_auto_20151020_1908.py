# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0035_auto_20151020_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_insumo', models.PositiveIntegerField()),
                ('insumo', models.ForeignKey(to='recetas.Insumo')),
                ('pedido_proveedor', models.ForeignKey(to='recetas.PedidoProveedor')),
            ],
        ),
        migrations.AddField(
            model_name='pedidoproveedor',
            name='insumos',
            field=models.ManyToManyField(to='recetas.Insumo', through='recetas.DetallePedidoProveedor'),
        ),
    ]
