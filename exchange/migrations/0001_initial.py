# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('google_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('published_date', models.IntegerField()),
                ('description', models.TextField()),
                ('page_count', models.IntegerField()),
                ('dim_height', models.CharField(max_length=50)),
                ('dim_width', models.CharField(max_length=50)),
                ('dim_thickness', models.CharField(max_length=50)),
                ('print_type', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=50)),
                ('img_small_thumbnail', models.CharField(max_length=1000)),
                ('img_thumbnail', models.CharField(max_length=1000)),
                ('img_small', models.CharField(max_length=1000)),
                ('img_medium', models.CharField(max_length=1000)),
                ('img_large', models.CharField(max_length=1000)),
                ('img_extra_large', models.CharField(max_length=1000)),
                ('authors', models.ManyToManyField(to='exchange.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('text', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(to='exchange.Book')),
                ('lendee', models.ForeignKey(related_name='lent_book', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='owned_book', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_picture', image_cropping.fields.ImageCropField(null=True, upload_to=b'profile_pictures', blank=True)),
                (b'cropping', image_cropping.fields.ImageRatioField(b'profile_picture', '430x430', hide_image_field=False, size_warning=True, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping')),
                ('name', models.CharField(max_length=100, verbose_name=b'full name', blank=True)),
                ('address_line_1', models.CharField(max_length=50, verbose_name=b'address line 1', blank=True)),
                ('address_line_2', models.CharField(max_length=50, verbose_name=b'address line 2', blank=True)),
                ('address_city', models.CharField(max_length=50, verbose_name=b'city', blank=True)),
                ('address_state', models.CharField(max_length=50, verbose_name=b'state', blank=True)),
                ('address_code', models.CharField(max_length=50, verbose_name=b'postal code', blank=True)),
                ('address_country', models.CharField(max_length=50, verbose_name=b'country', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='book',
            field=models.ForeignKey(to='exchange.UserBook'),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='category_book', to='exchange.Category'),
        ),
    ]
