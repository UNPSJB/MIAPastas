# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0006_auto_20151024_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoclientedetalle',
            name='cantidad_producto',
            field=models.FloatField(),
        ),
    ]
