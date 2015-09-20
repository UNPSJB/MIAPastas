# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_auto_20150919_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(help_text=b'La razon social del proveedor', unique=True, max_length=100)),
                ('nombreDueno', models.CharField(help_text=b'El nombre del due\xc3\xb1o', unique=True, max_length=100)),
                ('direccion', models.CharField(help_text=b'la direccion', unique=True, max_length=100)),
                ('email', models.CharField(help_text=b'El email del proveedor', unique=True, max_length=30)),
                ('localidad', models.CharField(help_text=b'La localidad donde se encuantra el proveedor', unique=True, max_length=50)),
                ('numeroCuenta', models.PositiveIntegerField()),
                ('provincia', models.CharField(help_text=b'La provincia', unique=True, max_length=50)),
                ('telefono', models.PositiveIntegerField()),
                ('cuit', models.PositiveIntegerField(help_text=b'El cuit del proveedor')),
                ('insumos', models.ManyToManyField(related_name='proveedores', to='recetas.Insumo')),
            ],
        ),
    ]
