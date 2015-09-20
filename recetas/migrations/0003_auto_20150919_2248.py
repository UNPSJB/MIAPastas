# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20150918_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoTerminado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text=b'El nombre del insumo', unique=True, max_length=100)),
                ('stock', models.IntegerField()),
                ('unidad_medida', models.PositiveSmallIntegerField(choices=[(3, b'Unidad'), (5, b'Bolson'), (1, b'Kg'), (5, b'Bolsines')])),
                ('precio', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.AlterField(
            model_name='receta',
            name='nombre',
            field=models.CharField(help_text=b'El nombre de la receta', unique=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receta',
            name='productoTerminado',
            field=models.ForeignKey(to='recetas.ProductoTerminado', null=True),
        ),
    ]
