# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0022_auto_20151014_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='zona',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
