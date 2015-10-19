# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0028_auto_20151018_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='fecha_realizacion',
            field=models.DateField(),
        ),
    ]
