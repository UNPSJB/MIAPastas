# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocliente',
            name='tipo_pedido',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'Pedido Fijo'), (2, b'Pedido Ocasional'), (3, b'Pedido de Cambio')]),
            preserve_default=False,
        ),
    ]
