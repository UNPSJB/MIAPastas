# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151104_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductosExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.FloatField()),
                ('hoja_de_ruta', models.ForeignKey(to='recetas.HojaDeRuta')),
                ('producto_terminado', models.ForeignKey(default=None, to='recetas.ProductoTerminado')),
            ],
        ),
        migrations.CreateModel(
            name='ProductosExtraDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('lote', models.ForeignKey(to='recetas.Lote')),
                ('lote_extra', models.ForeignKey(to='recetas.ProductosExtra')),
            ],
        ),
        migrations.RemoveField(
            model_name='lotesextra',
            name='hoja_de_ruta',
        ),
        migrations.RemoveField(
            model_name='lotesextra',
            name='lote',
        ),
        migrations.DeleteModel(
            name='LotesExtra',
        ),
    ]
