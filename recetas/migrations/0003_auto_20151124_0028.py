# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151122_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerdidaStockLote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_perdida', models.PositiveIntegerField()),
                ('motivo', models.CharField(max_length=100)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hoja_de_ruta', models.ForeignKey(blank=True, to='recetas.HojaDeRuta', null=True)),
                ('lote', models.ForeignKey(to='recetas.Lote')),
            ],
        ),
        migrations.RemoveField(
            model_name='loteentregadetalle',
            name='entrega_detalle',
        ),
        migrations.RemoveField(
            model_name='loteentregadetalle',
            name='lote',
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 24)),
        ),
        migrations.DeleteModel(
            name='LoteEntregaDetalle',
        ),
    ]
