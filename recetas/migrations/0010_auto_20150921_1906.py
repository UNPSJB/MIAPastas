# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0009_auto_20150921_1900'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receta',
            old_name='itemDetalle',
            new_name='items',
        ),
    ]
