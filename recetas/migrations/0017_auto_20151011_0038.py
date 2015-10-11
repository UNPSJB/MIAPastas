# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0016_auto_20151009_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoterminado',
            name='nombre',
            field=models.CharField(help_text=b'El nombre del producto', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='recetadetalle',
            name='cantidad_insumo',
            field=models.PositiveIntegerField(),
        ),
    ]
