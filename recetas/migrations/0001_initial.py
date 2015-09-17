# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
                ('descripcion', models.TextField()),
                ('stock', models.PositiveIntegerField()),
                ('unidad_medida', models.PositiveSmallIntegerField(choices=[(1, b'Kg'), (2, b'Litro'), (3, b'Unidad'), (4, b'Docena'), (5, b'Caja')])),
            ],
        ),
    ]
