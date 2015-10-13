# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0018_auto_20151012_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoterminado',
            name='precio',
            field=models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
    ]
