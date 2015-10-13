# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0017_auto_20151012_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoterminado',
            name='precio',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
