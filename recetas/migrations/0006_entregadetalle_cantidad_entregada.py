# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0005_auto_20151104_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregadetalle',
            name='cantidad_entregada',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
