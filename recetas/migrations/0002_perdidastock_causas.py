# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perdidastock',
            name='causas',
            field=models.PositiveSmallIntegerField(default=1, choices=[(b'1', b'Vencimiento'), (b'2', b'Rotura'), (b'3', b'Otros')]),
        ),
    ]
