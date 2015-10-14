# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0020_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='codigo_postal',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
