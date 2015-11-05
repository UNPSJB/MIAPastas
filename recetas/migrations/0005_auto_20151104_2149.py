# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151104_1137'),
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
                ('cantidad_enviada', models.PositiveIntegerField()),
                ('precio', models.PositiveIntegerField()),
                ('entrega', models.ForeignKey(to='recetas.Entrega')),
                ('pedido_cliente_detalle', models.ForeignKey(to='recetas.PedidoClienteDetalle')),
            ],
        ),
        migrations.CreateModel(
            name='LoteEntregaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('lote', models.ForeignKey(to='recetas.Lote')),
            ],
        ),
        migrations.RenameModel(
            old_name='ProductosExtra',
            new_name='ProductoExtra',
        ),
        migrations.RenameField(
            model_name='productosextradetalle',
            old_name='lote_extra',
            new_name='producto_extra',
        ),
    ]
