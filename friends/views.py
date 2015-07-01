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

class FriendsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friends/friends_list.html"

    def get_context_object_name(self, obj):
        return "user_list"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FriendsListView, self).get_context_data(**kwargs)
        context['friends_username'] = self.kwargs['username']
        if self.kwargs['username'] != self.request.user.username:
            context['user_pending_requests'] = Friend.objects.unrejected_requests(user=self.request.user)
            context['user_sent_requests'] = Friend.objects.sent_requests(user=self.request.user)
            context['pending_requests_users'] = [fr.from_user for fr in context['user_pending_requests']]
            context['sent_requests_users'] = [fr.to_user for fr in context['user_sent_requests']]
            context['user_friends'] = Friend.objects.friends(user=self.request.user)
        return context

    def get_queryset(self, **kwargs):
        return Friend.objects.friends(user=get_object_or_404(User, username=self.kwargs['username']))

@require_http_methods(['GET', 'POST'])
def unfriend(request, username):
    other_user = get_object_or_404(User, username=username)

    # make sure this friendship exists
    if not Friend.objects.are_friends(request.user, other_user):
        messages.error(request, 'Couldn\'t remove friend.')
        return redirect('friends_list', request.user.username)

    if request.method == 'GET':
        # display page to confirm deletion
        return render(request, "friends/unfriend.html", {'other_user': other_user})
    else: # POST
        # perform deletion, redirect to friends list
        messages.info(request, 'Removed friend.')
        Friend.objects.remove_friend(other_user, request.user)
        return redirect('friends_list', request.user.username)

class FriendshipRequestsListView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = "friends/friendshiprequest_list.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FriendshipRequestsListView, self).get_context_data(**kwargs)
        # the type of friend requests displayed (unread, read, etc.)
        t = self.kwargs['t']
        if t == 'sent':
            context['t'] = 'sent'
        elif t == 'pending':
            context['t'] = 'pending'
        elif t == 'rejected':
            context['t'] = 'rejected'
        else:
            context['t'] = 'all'

        context['received_friend_request_count'] = len(Friend.objects.requests(user=self.request.user))
        context['sent_friend_request_count'] = len(Friend.objects.sent_requests(user=self.request.user))
        context['rejected_friend_request_count'] = len(Friend.objects.rejected_requests(user=self.request.user))
        context['pending_friend_request_count'] = Friend.objects.unrejected_request_count(user=self.request.user)
        context['all_friend_request_count'] = context['sent_friend_request_count'] + context['received_friend_request_count']

        return context

    def get_context_object_name(self, obj):
        return "friendshiprequest_list"

    def get_queryset(self, **kwargs):
        t = self.kwargs['t']
        if t == 'sent':
            return Friend.objects.sent_requests(user=self.request.user)
        elif t == 'rejected':
            return Friend.objects.rejected_requests(user=self.request.user)
        elif t == 'pending':
            # mark all unread requests as viewed
            friendship_request_list = Friend.objects.unrejected_requests(user=self.request.user)
            for fr in friendship_request_list:
                if not fr.viewed:
                    fr.mark_viewed()
            return friendship_request_list
        else:
            friendship_request_list = Friend.objects.requests(user=self.request.user) + Friend.objects.sent_requests(user=self.request.user)
            for fr in friendship_request_list:
                if not fr.viewed:
                    fr.mark_viewed()
            return sorted(friendship_request_list, key=lambda x: x.rejected if x.rejected else x.created, reverse=True)

class FriendshipRequestsDetailView(LoginRequiredMixin, DetailView):
    model = FriendshipRequest
    template_name = "friends/friendshiprequest_detail.html"

    def get_context_object_name(self, obj):
        return "friendshiprequest"

@login_required
@require_http_methods(['POST'])
def friendship_requests_send(request, to_pk):
    other_user = get_object_or_404(User, pk=to_pk)

    # check to make sure a friend request has not already been sent
    sent_requests = Friend.objects.sent_requests(user=request.user)
    for fr in sent_requests:
        if fr.to_user == other_user:
            messages.error(request, 'Friend request already sent.')
            return redirect('friendship_requests_detail', fr.pk)

    friendship_request = Friend.objects.add_friend(request.user, other_user)
    return redirect('friendship_requests_detail', friendship_request.pk)

@login_required
@require_http_methods(['POST'])
def friendship_requests_cancel(request, pk):
    friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
    if friendship_request.from_user == request.user:
        friendship_request.cancel()
        messages.info(request, 'Friend request canceled.')
        return redirect('friendship_requests_list', t='sent')
    else:
        messages.error(request, 'Error canceling friend request.')
        return redirect('friendship_requests_list', t='sent')

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
        return redirect('friendship_requests_list', t='pending')

@login_required
@require_http_methods(['POST'])
def friendship_requests_reject(request, pk):
    friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
    if friendship_request.to_user == request.user:
        friendship_request.reject()
        return redirect('friendship_requests_list', t='pending')
    else:
        messages.error(request, 'Error rejecting friend request.')
        return redirect('friendship_requests_list', t='pending')
