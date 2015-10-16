# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0023_zona_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='nombre_dueno',
            field=models.CharField(max_length=100),
        ),
    ]
