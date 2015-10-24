# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20151024_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoclientedetalle',
            name='cantidad_producto',
            field=models.DecimalField(max_digits=5, decimal_places=2),
        ),
    ]
