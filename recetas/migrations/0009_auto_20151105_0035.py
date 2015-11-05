# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0008_auto_20151104_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregadetalle',
            name='cantidad_enviada',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 5)),
        ),
    ]
