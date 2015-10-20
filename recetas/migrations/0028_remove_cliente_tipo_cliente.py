# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0027_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='tipo_cliente',
        ),
    ]
