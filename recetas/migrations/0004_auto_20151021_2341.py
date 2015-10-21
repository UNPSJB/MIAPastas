# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20151021_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lote',
            old_name='id',
            new_name='nro_lote',
        ),
    ]
