# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoterminado',
            name='dias_vigencia',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 2)),
        ),
    ]
