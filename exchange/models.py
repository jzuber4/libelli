from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class UserProfile(models.Model):
    user            = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
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
