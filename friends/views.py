from braces.views import LoginRequiredMixin
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from friendship.models import FriendshipRequest, Friend

class FriendshipRequestsListView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = "friends/friendshiprequest_list.html"

    def get_context_object_name(self, obj):
        return "friendshiprequest_list"

    def get_queryset(self, **kwargs):
        if self.request.GET.get('t') == 'sent':
            return Friend.objects.sent_requests(user=self.request.user)
        elif self.request.GET.get('t') == 'received':
            return Friend.objects.requests(user=self.request.user)
        elif self.request.GET.get('t') == 'rejected':
            return Friend.objects.rejected_requests(user=self.request.user)
        elif self.request.GET.get('t') == 'unrejected':
            return Friend.objects.unrejected_requests(user=self.request.user)
        elif self.request.GET.get('t') == 'unread':
            return Friend.objects.unread_requests(user=self.request.user)
        elif self.request.GET.get('t') == 'read':
            return Friend.objects.read_requests(user=self.request.user)
        else:
            friendshiprequest_list = Friend.objects.requests(user=self.request.user) + Friend.objects.sent_requests(user=self.request.user)
            return sorted(friendshiprequest_list, key=lambda x: x.rejected if x.rejected else x.created, reverse=True)

class FriendshipRequestsDetailView(LoginRequiredMixin, DetailView):
    model = FriendshipRequest
    template_name = "friends/friendshiprequest_detail.html"

    def get_context_object_name(self, obj):
        return "friendshiprequest"

@login_required
@require_http_methods(['POST'])
def friendship_requests_send(request, to_pk):
    friendship_request = Friend.objects.add_friend(request.user, get_object_or_404(User, pk=to_pk))
    return redirect('friendship_requests_detail', friendship_request.pk)

@login_required
@require_http_methods(['POST'])
def friendship_requests_cancel(request, pk):
    friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
    if friendship_request.from_user == request.user:
        friendship_request.cancel()
        messages.info(request, 'Friend request canceled.')
        return redirect('friendship_requests_list')
    else:
        messages.error(request, 'Error canceling friend request.')
        return redirect('friendship_requests_list')

@login_required
@require_http_methods(['POST'])
def friendship_requests_accept(request, pk):
    friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
    if friendship_request.to_user == request.user:
        friendship_request.accept()
        messages.info(request, 'You are now friends with {}!'.format(friendship_request.from_user.username))
        return redirect('profile', friendship_request.from_user.username)
    else:
        messages.error(request, 'Error accepting friend request.')
        return redirect('friendship_requests_list')

@login_required
@require_http_methods(['POST'])
def friendship_requests_reject(request, pk):
    friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
    if friendship_request.to_user == request.user:
        friendship_request.reject()
        return redirect('friendship_requests_list')
    else:
        messages.error(request, 'Error rejecting friend request.')
        return redirect('friendship_requests_list')








