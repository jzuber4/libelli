"""Friend request app URLs
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/(?P<username>[\w-]+)/$', views.FriendsListView.as_view(), name='friends_list'),
    url(r'^unfriend/(?P<username>[\w-]+)/$', views.unfriend, name='friends_unfriend'),
    url(r'^requests/(?P<pk>\d+)/$', views.FriendshipRequestsDetailView.as_view(), name='friendship_requests_detail'),
    url(r'^requests/(?P<t>\w+)/$', views.FriendshipRequestsListView.as_view(), name='friendship_requests_list'),
    url(r'^requests/(?P<to_pk>\d+)/send/$', views.friendship_requests_send, name='friendship_requests_send'),
    url(r'^requests/(?P<pk>\d+)/cancel/$', views.friendship_requests_cancel, name='friendship_requests_cancel'),
    url(r'^requests/(?P<pk>\d+)/accept/$', views.friendship_requests_accept, name='friendship_requests_accept'),
    url(r'^requests/(?P<pk>\d+)/reject/$', views.friendship_requests_reject, name='friendship_requests_reject'),
]
