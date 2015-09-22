# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0008_auto_20150920_0147'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecetaDetalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidadInsumo', models.IntegerField()),
                ('insumo', models.ForeignKey(to='recetas.Insumo')),
            ],
        ),
        migrations.RemoveField(
            model_name='receta',
            name='insumos',
        ),
        migrations.AddField(
            model_name='recetadetalle',
            name='receta',
            field=models.ForeignKey(to='recetas.Receta'),
        ),
        migrations.AddField(
            model_name='receta',
            name='itemDetalle',
            field=models.ManyToManyField(to='recetas.Insumo', through='recetas.RecetaDetalle'),
        ),
    ]
