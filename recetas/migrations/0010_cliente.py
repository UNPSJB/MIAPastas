# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0009_auto_20150921_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuit_cuil', models.PositiveIntegerField()),
                ('razonSocial', models.CharField(unique=True, max_length=100)),
                ('nombreDueno', models.CharField(unique=True, max_length=100)),
                ('tipo_cliente', models.PositiveSmallIntegerField(choices=[(1, b'Cliente Fijo'), (2, b'Cliente Ocasional')])),
                ('direccion', models.CharField(unique=True, max_length=100)),
                ('telefono', models.PositiveIntegerField()),
                ('email', models.CharField(max_length=30, unique=True, null=True, blank=True)),
                ('esMoroso', models.BooleanField(default=False)),
                ('ciudad', models.ForeignKey(to='recetas.Ciudad')),
            ],
        ),
    ]
