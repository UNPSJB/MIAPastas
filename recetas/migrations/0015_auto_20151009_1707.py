# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0014_auto_20151005_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuit', models.CharField(unique=True, max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.PositiveIntegerField()),
                ('e_mail', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='productoterminado',
            name='nombre',
            field=models.CharField(help_text=b'El nombre del producto', unique=True, max_length=100),
        ),
    ]
