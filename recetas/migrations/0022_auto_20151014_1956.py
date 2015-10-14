# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0021_auto_20151013_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cuit_cuil',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='cuit',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='numero_cuenta',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='receta',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Kg'), (2, b'Unidad'), (3, b'Bolson'), (4, b'Bolsines')]),
        ),
    ]
