# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='dim_height',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='dim_thickness',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='dim_width',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='img_extra_large',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='img_large',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='img_medium',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='img_small',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='img_small_thumbnail',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='img_thumbnail',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
