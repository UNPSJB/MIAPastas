# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0007_auto_20150920_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='productoTerminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado'),
        ),
    ]
