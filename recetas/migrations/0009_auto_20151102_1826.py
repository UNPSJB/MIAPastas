# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0008_auto_20151102_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoterminado',
            name='unidad_medida',
        ),
        migrations.AlterField(
            model_name='productoterminado',
            name='dias_vigencia',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
