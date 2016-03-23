# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0002_auto_20160204_0651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='lendee',
        ),
        migrations.AddField(
            model_name='userbook',
            name='holder',
            field=models.ForeignKey(related_name='held_book', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
