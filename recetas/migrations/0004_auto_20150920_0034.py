# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20150919_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receta',
            old_name='Descripcion',
            new_name='descripcion',
        ),
    ]
