# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0008_auto_20151101_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='fecha_cancelacion',
            field=models.DateField(null=True, blank=True),
        ),
    ]
