# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuit', models.CharField(unique=True, max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.PositiveIntegerField()),
                ('e_mail', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
                ('codigo_postal', models.PositiveIntegerField(unique=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuit', models.PositiveIntegerField(unique=True)),
                ('razon_social', models.CharField(unique=True, max_length=100)),
                ('nombre_dueno', models.CharField(max_length=100)),
                ('direccion', models.CharField(unique=True, max_length=100)),
                ('telefono', models.PositiveIntegerField()),
                ('email', models.CharField(max_length=30, null=True, blank=True)),
                ('es_moroso', models.BooleanField(default=False)),
                ('saldo', models.FloatField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(to='recetas.Ciudad')),
            ],
            options={
                'permissions': (('ver_clientes_morosos', 'Puede listar los clientes morosos'),),
            },
        ),
        migrations.CreateModel(
            name='DetallePedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_insumo', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntregaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_enviada', models.PositiveIntegerField(null=True)),
                ('cantidad_entregada', models.PositiveIntegerField(null=True)),
                ('precio', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)])),
                ('entrega', models.ForeignKey(to='recetas.Entrega')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numero', models.PositiveIntegerField()),
                ('monto_pagado', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)])),
            ],
        ),
        migrations.CreateModel(
            name='HojaDeRuta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('rendida', models.BooleanField(default=False)),
                ('chofer', models.ForeignKey(to='recetas.Chofer')),
            ],
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text=b'El nombre del insumo', unique=True, max_length=100)),
                ('descripcion', models.TextField(verbose_name=b'Descripc\xc3\xb3n')),
                ('stock', models.IntegerField(default=0, null=True, blank=True)),
                ('unidad_medida', models.PositiveSmallIntegerField(choices=[(1, b'g'), (2, b'cm3'), (3, b'unidad')])),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('nro_lote', models.AutoField(serialize=False, primary_key=True)),
                ('fecha_produccion', models.DateField()),
                ('fecha_vencimiento', models.DateField()),
                ('cantidad_producida', models.PositiveIntegerField()),
                ('stock_disponible', models.PositiveIntegerField()),
                ('stock_reservado', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LoteEntregaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('entrega_detalle', models.ForeignKey(to='recetas.EntregaDetalle')),
                ('lote', models.ForeignKey(to='recetas.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('tipo_pedido', models.PositiveSmallIntegerField(choices=[(1, b'Pedido Fijo'), (2, b'Pedido Ocasional'), (3, b'Pedido de Cambio')])),
                ('activo', models.BooleanField(default=True)),
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
            name='PedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_realizacion', models.DateField()),
                ('fecha_de_entrega', models.DateField(null=True, blank=True)),
                ('estado_pedido', models.PositiveSmallIntegerField(default=b'1', choices=[(1, b'Pendiente'), (2, b'Recibido'), (3, b'Cancelado')])),
                ('descripcion', models.TextField(null=True)),
                ('fecha_cancelacion', models.DateField(null=True, blank=True)),
                ('insumos', models.ManyToManyField(to='recetas.Insumo', through='recetas.DetallePedidoProveedor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductosLlevados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_pedida', models.PositiveIntegerField(default=0)),
                ('cantidad_enviada', models.PositiveIntegerField(default=0)),
                ('hoja_de_ruta', models.ForeignKey(to='recetas.HojaDeRuta')),
            ],
        ),
        migrations.CreateModel(
            name='ProductosLlevadosDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('cantidad_sobrante', models.PositiveIntegerField(null=True)),
                ('lote', models.ForeignKey(to='recetas.Lote')),
                ('producto_llevado', models.ForeignKey(to='recetas.ProductosLlevados')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoTerminado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text=b'El nombre del producto', unique=True, max_length=100)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('precio', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)])),
                ('dias_vigencia', models.PositiveIntegerField(default=1)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razon_social', models.CharField(unique=True, max_length=100)),
                ('nombre_dueno', models.CharField(unique=True, max_length=100)),
                ('direccion', models.CharField(unique=True, max_length=100)),
                ('email', models.CharField(max_length=30, unique=True, null=True, blank=True)),
                ('localidad', models.CharField(unique=True, max_length=50)),
                ('numero_cuenta', models.PositiveIntegerField(unique=True)),
                ('provincia', models.CharField(unique=True, max_length=50)),
                ('telefono', models.PositiveIntegerField()),
                ('cuit', models.PositiveIntegerField(unique=True)),
                ('activo', models.BooleanField(default=True)),
                ('insumos', models.ManyToManyField(related_name='proveedores', to='recetas.Insumo')),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('nombre', models.CharField(help_text=b'El nombre de la receta', unique=True, max_length=100)),
                ('descripcion', models.TextField()),
                ('cant_prod_terminado', models.PositiveIntegerField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecetaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_insumo', models.PositiveIntegerField()),
                ('insumo', models.ForeignKey(to='recetas.Insumo')),
                ('receta', models.ForeignKey(to='recetas.Receta')),
            ],
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numero', models.PositiveIntegerField()),
                ('monto_pagado', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)])),
                ('entrega', models.ForeignKey(to='recetas.Entrega')),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
                ('activo', models.BooleanField(default=True)),
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
                ('fecha_inicio', models.DateField(default=datetime.date(2015, 11, 19))),
                ('fecha_cancelacion', models.DateField(null=True, blank=True)),
                ('dias', multiselectfield.db.fields.MultiSelectField(max_length=9, choices=[(1, b'lunes'), (2, b'martes'), (3, b'miercoles'), (4, b'jueves'), (5, b'viernes')])),
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
            model_name='receta',
            name='insumos',
            field=models.ManyToManyField(to='recetas.Insumo', through='recetas.RecetaDetalle'),
        ),
        migrations.AddField(
            model_name='receta',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado'),
        ),
        migrations.AddField(
            model_name='productosllevados',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado'),
        ),
        migrations.AddField(
            model_name='pedidoproveedor',
            name='proveedor',
            field=models.ForeignKey(to='recetas.Proveedor'),
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
        migrations.AddField(
            model_name='lote',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado'),
        ),
        migrations.AddField(
            model_name='entregadetalle',
            name='pedido_cliente_detalle',
            field=models.ForeignKey(blank=True, to='recetas.PedidoClienteDetalle', null=True),
        ),
        migrations.AddField(
            model_name='entregadetalle',
            name='producto_terminado',
            field=models.ForeignKey(blank=True, to='recetas.ProductoTerminado', null=True),
        ),
        migrations.AddField(
            model_name='entrega',
            name='factura',
            field=models.ForeignKey(to='recetas.Factura', null=True),
        ),
        migrations.AddField(
            model_name='entrega',
            name='hoja_de_ruta',
            field=models.ForeignKey(to='recetas.HojaDeRuta'),
        ),
        migrations.AddField(
            model_name='entrega',
            name='pedido',
            field=models.ForeignKey(to='recetas.PedidoCliente'),
        ),
        migrations.AddField(
            model_name='detallepedidoproveedor',
            name='insumo',
            field=models.ForeignKey(to='recetas.Insumo'),
        ),
        migrations.AddField(
            model_name='detallepedidoproveedor',
            name='pedido_proveedor',
            field=models.ForeignKey(to='recetas.PedidoProveedor'),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='zona',
            field=models.ForeignKey(related_name='ciudades', to='recetas.Zona'),
        ),
    ]
