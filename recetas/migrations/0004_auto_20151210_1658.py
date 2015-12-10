# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20151211_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chofer',
            name='e_mail',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='monto_pagado',
            field=models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 1)]),
        ),
        migrations.AlterField(
            model_name='factura',
            name='numero',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 12, 10)),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(default=datetime.datetime(2015, 12, 10, 19, 58, 53, 624000, tzinfo=utc), unique=True, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recibo',
            name='numero',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
