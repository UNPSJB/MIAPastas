# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0009_auto_20151101_2201'),
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
            name='LotesExtraDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.FloatField()),
                ('hoja_de_ruta', models.ForeignKey(to='recetas.HojaDeRuta')),
                ('lote', models.ForeignKey(to='recetas.Lote')),
            ],
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 2)),
        ),
        migrations.AddField(
            model_name='hojaderuta',
            name='lote_extra',
            field=models.ManyToManyField(to='recetas.Lote', through='recetas.LotesExtraDetalle'),
        ),
    ]
