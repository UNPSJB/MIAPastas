# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0010_auto_20150921_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receta',
            old_name='items',
            new_name='insumos',
        ),
    ]
