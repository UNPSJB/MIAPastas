# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidoproveedor',
            name='fecha_cancelacion',
            field=models.DateField(default=datetime.datetime(2015, 11, 2, 0, 34, 44, 968000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 1)),
        ),
    ]
