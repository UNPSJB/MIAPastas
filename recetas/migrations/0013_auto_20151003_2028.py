# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0012_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ciudad',
            old_name='codigoPostal',
            new_name='codigo_postal',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='esMoroso',
            new_name='es_moroso',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='nombreDueno',
            new_name='nombre_dueno',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='razonSocial',
            new_name='razon_social',
        ),
        migrations.RenameField(
            model_name='proveedor',
            old_name='nombreDueno',
            new_name='nombre_dueno',
        ),
        migrations.RenameField(
            model_name='proveedor',
            old_name='numeroCuenta',
            new_name='numero_cuenta',
        ),
        migrations.RenameField(
            model_name='proveedor',
            old_name='razonSocial',
            new_name='razon_social',
        ),
        migrations.RenameField(
            model_name='receta',
            old_name='cantProdTerminado',
            new_name='cant_prod_terminado',
        ),
        migrations.RenameField(
            model_name='receta',
            old_name='fechaCreacion',
            new_name='fecha_creacion',
        ),
        migrations.RenameField(
            model_name='receta',
            old_name='productoTerminado',
            new_name='producto_terminado',
        ),
        migrations.RenameField(
            model_name='recetadetalle',
            old_name='cantidadInsumo',
            new_name='cantidad_insumo',
        ),
    ]
