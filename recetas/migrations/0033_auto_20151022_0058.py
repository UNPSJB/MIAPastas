# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0032_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidofijo',
            name='dias',
            field=multiselectfield.db.fields.MultiSelectField(max_length=9, choices=[(1, b'lunes'), (2, b'martes'), (3, b'miercoles'), (4, b'jueves'), (5, b'viernes')]),
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 10, 22)),
        ),
        migrations.DeleteModel(
            name='DiasSemana',
        ),
    ]
