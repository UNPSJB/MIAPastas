# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20151104_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productosextra',
            name='producto_terminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado'),
        ),
    ]
