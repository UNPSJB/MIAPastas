# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0015_auto_20151012_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoterminado',
            name='stock',
            field=models.PositiveIntegerField(),
        ),
    ]
