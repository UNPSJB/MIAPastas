# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20151021_2341'),
    ]

    operations = [

        migrations.AlterField(
            model_name='lote',
            name='nro_lote',
            field=models.AutoField(primary_key=True, db_column='nro_lote'),
        ),
    ]
