# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0024_auto_20151016_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zona',
            name='activo',
        ),
    ]
