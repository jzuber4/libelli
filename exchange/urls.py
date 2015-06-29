"""Exchange app URLs
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>[\w-]+)/$', views.UserProfileDetailView.as_view(), name='profile'),
    url(r'^profile/edit$', views.UserProfileUpdateView.as_view(), name='edit_profile'),
    url(r'^profile/edit/picture$', views.UserProfilePictureUpdateView.as_view(), name='edit_profile_picture'),
]
