from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

from image_cropping import ImageCropField, ImageRatioField

import requests

class AuthorManager(models.Manager):
    def get_or_create(self, name):
        author = self.filter(name=name)
        if len(author) == 1:
            return author[0], False
        else:
            return self.create(name=name), True

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = AuthorManager()

    def __str__(self):
        return self.name

class CategoryManager(models.Manager):
    def get_or_create(self, name):
        category = self.filter(name=name)
        if len(category) == 1:
            return category[0], False
        else:
            return self.create(name=name), True

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = CategoryManager()

    def __str__(self):
        return self.name

class BookManager(models.Manager):
    def get_or_create(self, google_id):
        book = self.filter(google_id=google_id)
        if len(book) == 1:
            return book[0], False
        else:
            return self.create_book(google_id), True

    def create_book(self, google_id):
        volume = requests.get('https://www.googleapis.com/books/v1/volumes/' + google_id
                + '?key=' + settings.GOOGLE_BOOKS_API_KEY).json()

        volume_info = volume.get('volumeInfo')

        # get and (maybe) create Authors / Categories
        authors = [a for a in volume_info['authors']] if volume_info.get('authors') else []
        categories = [c for c in volume_info['categories']] if volume_info.get('categories') else []
        authors = [Author.objects.get_or_create(a) for a in authors]
        categories = [Category.objects.get_or_create(c) for c in categories]
        authors = [a for a, created in authors]
        categories = [c for c, created in  categories]

        # return empty string if None, otherwise return the value
        maybe = lambda s: s if s else ''

        book = Book()
        book.google_id = google_id
        book.title = volume_info.get('title')
        book.publisher = volume_info.get('publisher')
        book.published_date = str(volume_info.get('publishedDate'))[:4] if volume_info.get('publishedDate') else None
        book.description = volume_info.get('description')
        book.page_count = volume_info.get('pageCount')
        dimensions = volume_info.get('dimensions')
        if dimensions:
            book.height = dimensions.get('height')
            book.width = dimensions.get('width')
            book.thickness = dimensions.get('thickness')
        book.print_type = volume_info.get('printType')
        book.language = volume_info.get('language')
        image_links = volume_info.get('imageLinks')
        if image_links:
            book.img_small_thumbnail = maybe(image_links.get('smallThumbnail'))
            book.img_thumbnail = maybe(image_links.get('thumbnail'))
            book.img_small = maybe(image_links.get('small'))
            book.img_medium = maybe(image_links.get('medium'))
            book.img_large = maybe(image_links.get('large'))
            book.img_extra_large = maybe(image_links.get('extraLarge'))

        book.save()
        book.categories = categories
        book.authors = authors
        book.save()
        return book


class Book(models.Model):
    google_id      = models.CharField(max_length=100, unique=True)
    title          = models.CharField(max_length=200)
    authors        = models.ManyToManyField(Author)
    publisher      = models.CharField(max_length=200)
    published_date = models.IntegerField()
    description    = models.TextField()
    page_count     = models.IntegerField()
    dim_height     = models.CharField(max_length=50, default='')
    dim_width      = models.CharField(max_length=50, default='')
    dim_thickness  = models.CharField(max_length=50, default='')
    print_type     = models.CharField(max_length=50)
    categories     = models.ManyToManyField(Category, related_name='category_book')
    language       = models.CharField(max_length=50)
    img_small_thumbnail = models.CharField(max_length=1000, default='')
    img_thumbnail       = models.CharField(max_length=1000, default='')
    img_small           = models.CharField(max_length=1000, default='')
    img_medium          = models.CharField(max_length=1000, default='')
    img_large           = models.CharField(max_length=1000, default='')
    img_extra_large     = models.CharField(max_length=1000, default='')

    objects = BookManager()

class UserBook(models.Model):
    owner  = models.ForeignKey(User, related_name='owned_book')
    book   = models.ForeignKey(Book)
    holder = models.ForeignKey(User, related_name='held_book')

class Review(models.Model):
    author = models.ForeignKey(User)
    book   = models.ForeignKey(UserBook)
    rating = models.IntegerField()
    text   = models.TextField()

class UserProfile(models.Model):
    user            = models.OneToOneField(User)
    profile_picture = ImageCropField(upload_to="profile_pictures", blank=True, null=True)
    cropping        = ImageRatioField('profile_picture', '430x430', size_warning=True)
    name            = models.CharField(max_length=100, blank=True, verbose_name='full name')
    address_line_1  = models.CharField(max_length=50, blank=True, verbose_name='address line 1')
    address_line_2  = models.CharField(max_length=50, blank=True, verbose_name='address line 2')
    address_city    = models.CharField(max_length=50, blank=True, verbose_name='city')
    address_state   = models.CharField(max_length=50, blank=True, verbose_name='state')
    address_code    = models.CharField(max_length=50, blank=True, verbose_name='postal code')
    address_country = models.CharField(max_length=50, blank=True, verbose_name='country')

    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture:
                this.profile_picture.delete(save=False)
        except: pass # when new image then we do nothing, normal case
        super(UserProfile, self).save(*args, **kwargs)

# auto-create profiles on registration
@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(UserBook)
admin.site.register(Review)
