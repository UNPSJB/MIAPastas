# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0025_remove_zona_activo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_realizacion', models.DateField()),
                ('fecha_probable_entrega', models.DateField()),
                ('proveedor', models.ForeignKey(to='recetas.Proveedor')),
            ],
        ),
    ]
