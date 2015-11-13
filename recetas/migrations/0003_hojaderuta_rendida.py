# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151114_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='hojaderuta',
            name='rendida',
            field=models.BooleanField(default=False),
        ),
    ]
