# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productosllevados',
            name='cantidad',
        ),
        migrations.AddField(
            model_name='productosllevados',
            name='cantidad_enviada',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productosllevados',
            name='cantidad_pedida',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
