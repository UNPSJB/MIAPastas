# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0024_auto_20151016_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiasSemana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('tipo_pedido', models.PositiveSmallIntegerField(choices=[(1, b'Pedido Fijo'), (2, b'Pedido Ocasional'), (3, b'Pedido de Cambio')])),
            ],
        ),
        migrations.CreateModel(
            name='PedidoClienteDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_producto', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PedidoCambio',
            fields=[
                ('pedidocliente_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='recetas.PedidoCliente')),
                ('fecha_entrega', models.DateField()),
            ],
            bases=('recetas.pedidocliente',),
        ),
        migrations.CreateModel(
            name='PedidoFijo',
            fields=[
                ('pedidocliente_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='recetas.PedidoCliente')),
                ('fecha_inicio', models.DateField()),
                ('fecha_cancelacion', models.DateField(blank=True)),
                ('dias', models.ForeignKey(to='recetas.DiasSemana')),
            ],
            bases=('recetas.pedidocliente',),
        ),
        migrations.CreateModel(
            name='PedidoOcacional',
            fields=[
                ('pedidocliente_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='recetas.PedidoCliente')),
                ('fecha_entrega', models.DateField()),
            ],
            bases=('recetas.pedidocliente',),
        ),
        migrations.AddField(
            model_name='pedidoclientedetalle',
            name='pedido_cliente',
            field=models.ForeignKey(to='recetas.PedidoCliente'),
        ),
        migrations.AddField(
            model_name='pedidoclientedetalle',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado'),
        ),
        migrations.AddField(
            model_name='pedidocliente',
            name='cliente',
            field=models.ForeignKey(to='recetas.Cliente'),
        ),
        migrations.AddField(
            model_name='pedidocliente',
            name='productos',
            field=models.ManyToManyField(to='recetas.ProductoTerminado', through='recetas.PedidoClienteDetalle'),
        ),
    ]
