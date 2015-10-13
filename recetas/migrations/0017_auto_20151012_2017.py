# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0016_auto_20151012_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoterminado',
            name='precio',
            field=models.FloatField(),
        ),
    ]
