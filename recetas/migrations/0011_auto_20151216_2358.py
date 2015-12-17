# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0010_productosllevados_cantidad_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.CharField(max_length=50),
        ),
    ]
