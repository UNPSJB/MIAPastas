# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151029_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Kg'), (2, b'Litro'), (3, b'Unidad'), (4, b'Docena')]),
        ),
    ]
