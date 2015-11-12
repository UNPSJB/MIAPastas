# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='factura',
            field=models.ForeignKey(to='recetas.Factura', null=True),
        ),
    ]
