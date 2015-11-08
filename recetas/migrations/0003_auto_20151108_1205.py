# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151105_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregadetalle',
            name='precio',
            field=models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 8)),
        ),
    ]
