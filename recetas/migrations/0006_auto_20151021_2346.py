# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0005_auto_20151021_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='nro_lote',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
