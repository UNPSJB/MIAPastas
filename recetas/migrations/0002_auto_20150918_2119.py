# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaCreacion', models.DateField()),
                ('nombre', models.CharField(unique=True, max_length=100, verbose_name=b'El nombre de la receta')),
                ('unidad_medida', models.PositiveSmallIntegerField(choices=[(1, b'Kg'), (3, b'Unidad'), (5, b'Bolson'), (5, b'Bolsines')])),
                ('Descripcion', models.TextField()),
                ('cantProdTerminado', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='insumo',
            name='descripcion',
            field=models.TextField(verbose_name=b'Descripc\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='nombre',
            field=models.CharField(help_text=b'El nombre del insumo', unique=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receta',
            name='insumos',
            field=models.ManyToManyField(to='recetas.Insumo'),
        ),
    ]
