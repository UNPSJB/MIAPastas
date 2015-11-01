# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151029_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 10, 30)),
        ),
        migrations.AlterField(
            model_name='recetadetalle',
            name='cantidad_insumo',
            field=models.PositiveIntegerField(),
        ),
    ]
