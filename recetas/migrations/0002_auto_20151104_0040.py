# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HojaDeRuta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('chofer', models.ForeignKey(to='recetas.Chofer')),
            ],
        ),
        migrations.CreateModel(
            name='LotesExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.FloatField()),
                ('hoja_de_ruta', models.ForeignKey(to='recetas.HojaDeRuta')),
                ('lote', models.ForeignKey(to='recetas.Lote')),
            ],
        ),
        migrations.RemoveField(
            model_name='productoterminado',
            name='unidad_medida',
        ),
        migrations.RemoveField(
            model_name='receta',
            name='unidad_medida',
        ),
        migrations.AddField(
            model_name='pedidoproveedor',
            name='fecha_cancelacion',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='productoterminado',
            name='dias_vigencia',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='detallepedidoproveedor',
            name='cantidad_insumo',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='stock',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(1, b'g'), (2, b'cm3'), (3, b'unidad')]),
        ),
        migrations.AlterField(
            model_name='pedidoclientedetalle',
            name='cantidad_producto',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 4)),
        ),
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='recetadetalle',
            name='cantidad_insumo',
            field=models.PositiveIntegerField(),
        ),
    ]
