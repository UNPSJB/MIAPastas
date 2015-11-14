# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151110_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregadetalle',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado', null=True),
        ),
    ]
