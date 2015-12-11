# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perdidastocklote',
            name='hoja_de_ruta',
        ),
        migrations.RemoveField(
            model_name='perdidastocklote',
            name='lote',
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 12, 10)),
        ),
        migrations.DeleteModel(
            name='PerdidaStockLote',
        ),
    ]
