# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0014_auto_20151005_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoterminado',
            name='nombre',
            field=models.CharField(help_text=b'El nombre del producto', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='productoterminado',
            name='unidad_medida',
            field=models.PositiveSmallIntegerField(choices=[(2, b'Unidad'), (3, b'Bolson'), (1, b'Kg'), (4, b'Bolsines')]),
        ),
    ]
