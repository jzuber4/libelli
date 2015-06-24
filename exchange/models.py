from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    google_id      = models.CharField(max_length=100)
    title          = models.CharField(max_length=200)
    authors        = models.ManyToManyField(Author)
    publisher      = models.CharField(max_length=200)
    published_date = models.CharField(max_length=10) # yyyy-mm-dd
    description    = models.TextField()
    page_count     = models.IntegerField()
    dim_height     = models.CharField(max_length=50)
    dim_width      = models.CharField(max_length=50)
    dim_thickness  = models.CharField(max_length=50)
    print_type     = models.CharField(max_length=50)
    main_category  = models.ForeignKey(Category, related_name='main_category_book')
    categories     = models.ManyToManyField(Category, related_name='category_book')
    language       = models.CharField(max_length=50)
    img_small_thumbnail = models.ImageField()
    img_thumbnail       = models.ImageField()
    img_small           = models.ImageField()
    img_medium          = models.ImageField()
    img_large           = models.ImageField()
    img_extra_large     = models.ImageField()

class UserBook(models.Model):
    owner  = models.ForeignKey(User, related_name='owned_book')
    book   = models.ForeignKey(Book)
    lendee = models.ForeignKey(User, related_name='lent_book')

class Review(models.Model):
    author = models.ForeignKey(User)
    book   = models.ForeignKey(UserBook)
    rating = models.IntegerField()
    text   = models.TextField()

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(UserBook)
admin.site.register(Review)
