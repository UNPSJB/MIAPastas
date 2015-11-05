# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0006_entregadetalle_cantidad_entregada'),
    ]

    operations = [
        migrations.AddField(
            model_name='loteentregadetalle',
            name='entrega_detalle',
            field=models.ForeignKey(default=None, to='recetas.EntregaDetalle'),
        ),
    ]
