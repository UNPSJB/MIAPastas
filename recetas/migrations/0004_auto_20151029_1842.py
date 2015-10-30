# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20151029_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='stock',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(1, b'g'), (2, b'cm3'), (3, b'unidad')]),
        ),
    ]
