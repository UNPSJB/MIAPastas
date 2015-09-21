# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0006_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.CharField(max_length=30, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='receta',
            name='insumos',
            field=models.ManyToManyField(to='recetas.Insumo', blank=True),
        ),
    ]
