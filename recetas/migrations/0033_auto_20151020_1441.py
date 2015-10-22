# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0032_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidoproveedor',
            name='fecha_probable_entrega',
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='dias',
            field=models.ForeignKey(to='recetas.DiasSemana', blank=True),
        ),
    ]
