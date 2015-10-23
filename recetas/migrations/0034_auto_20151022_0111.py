# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0033_auto_20151022_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_cancelacion',
            field=models.DateField(null=True, blank=True),
        ),
    ]
