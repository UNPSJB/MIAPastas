# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0026_pedidoproveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidoproveedor',
            name='estado_pedido',
            field=models.PositiveSmallIntegerField(default=b'1', choices=[(1, b'Pendiente'), (2, b'Recibido'), (3, b'Cancelado')]),
        ),
        migrations.AddField(
            model_name='pedidoproveedor',
            name='fecha_de_entrega',
            field=models.DateField(null=True, blank=True),
        ),
    ]
