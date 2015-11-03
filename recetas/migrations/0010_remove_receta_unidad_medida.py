# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0009_auto_20151102_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receta',
            name='unidad_medida',
        ),
    ]
