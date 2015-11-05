# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0007_loteentregadetalle_entrega_detalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loteentregadetalle',
            name='entrega_detalle',
            field=models.ForeignKey(to='recetas.EntregaDetalle'),
        ),
    ]
