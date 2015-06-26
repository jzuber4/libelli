"""Exchange app URLs
"""
from django.conf.urls import url

from .views import index, user_profile_detail, user_profile_update

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^profile/(?P<username>[\w-]+)/$', user_profile_detail, name='profile'),
    url(r'^profile/edit$', user_profile_update, name='edit_profile'),
]
