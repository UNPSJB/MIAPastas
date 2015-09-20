# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20150918_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='nombre',
            field=models.CharField(help_text=b'El nombre de la receta', unique=True, max_length=100),
        ),
    ]
