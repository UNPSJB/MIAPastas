# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151110_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='chofer',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='zona',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 11)),
        ),
    ]
