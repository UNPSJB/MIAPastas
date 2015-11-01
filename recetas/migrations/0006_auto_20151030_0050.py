# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0005_auto_20151030_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedidoproveedor',
            name='cantidad_insumo',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='pedidoclientedetalle',
            name='cantidad_producto',
            field=models.PositiveIntegerField(),
        ),
    ]
