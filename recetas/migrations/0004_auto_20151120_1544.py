# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20151120_1119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='cuit',
            new_name='cuit',
        ),
        migrations.AddField(
            model_name='productosllevados',
            name='precio',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
    ]
