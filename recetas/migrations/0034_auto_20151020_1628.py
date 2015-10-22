# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0033_auto_20151020_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='fecha_de_entrega',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='fecha_realizacion',
            field=models.DateTimeField(),
        ),
    ]
