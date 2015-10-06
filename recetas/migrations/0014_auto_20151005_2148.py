# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0013_auto_20151003_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='zona',
            field=models.ForeignKey(related_name='ciudades', to='recetas.Zona'),
        ),
        migrations.AlterField(
            model_name='receta',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True),
        ),
    ]
