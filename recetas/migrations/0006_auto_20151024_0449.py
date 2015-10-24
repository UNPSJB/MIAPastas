# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0005_auto_20151024_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recetadetalle',
            name='cantidad_insumo',
            field=models.FloatField(),
        ),
    ]
