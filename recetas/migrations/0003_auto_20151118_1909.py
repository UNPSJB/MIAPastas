# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151117_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosllevados',
            name='precio',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 18)),
        ),
    ]
