# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151021_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lote',
            name='nro_lote',
        ),
        migrations.AlterField(
            model_name='lote',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='nro_lote'),
        ),
    ]
