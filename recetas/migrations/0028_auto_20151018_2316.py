# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0027_auto_20151018_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoproveedor',
            name='fecha_realizacion',
            field=models.DateTimeField(verbose_name=b'date published'),
        ),
    ]
