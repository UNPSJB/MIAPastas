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
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hoja_de_ruta', models.ForeignKey(to='recetas.HojaDeRuta')),
                ('pedido', models.ForeignKey(to='recetas.PedidoCliente')),
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
                ('pedido_cliente_detalle', models.ForeignKey(to='recetas.PedidoClienteDetalle')),
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
        migrations.RenameModel(
            old_name='ProductoExtra',
            new_name='ProductosLlevados',
        ),
        migrations.RenameModel(
            old_name='ProductosExtraDetalle',
            new_name='ProductosLlevadosDetalle',
        ),
        migrations.RenameField(
            model_name='productosllevadosdetalle',
            old_name='producto_extra',
            new_name='producto_llevado',
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 8)),
        ),
    ]
