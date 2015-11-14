# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_entregadetalle_producto_terminado'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosllevadosdetalle',
            name='cantidad_sobrante',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 12)),
        ),
    ]
