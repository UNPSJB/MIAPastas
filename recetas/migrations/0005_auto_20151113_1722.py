# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151112_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='saldo',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 13)),
        ),
    ]
