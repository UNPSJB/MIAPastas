# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_proveedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='cuit',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='direccion',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.CharField(max_length=30, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='localidad',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombreDueno',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='provincia',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='razonSocial',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
