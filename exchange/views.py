from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from friendship.models import Friend, FriendshipRequest

from .models import Author, Book, Category, UserBook, UserProfile

import requests

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['friends'] = Friend.objects.friends(context['userprofile'].user)
        context['is_friend'] = self.request.user in context['friends']
        context['user_books'] = UserBook.objects.filter(owner=context['userprofile'].user)
        if not context['is_friend']:
            sent_request = FriendshipRequest.objects.filter(from_user=self.request.user, to_user=context['userprofile'].user)
            received_request = FriendshipRequest.objects.filter(from_user=context['userprofile'].user, to_user=self.request.user)
            if sent_request.exists():
                context['sent_request'] = sent_request[0]
            elif received_request.exists() and not received_request[0].rejected:
                context['received_request'] = received_request[0]
        return context

    def get_object(self):
        username = self.kwargs['username'] if 'username' in self.kwargs else self.request.user.username
        return get_object_or_404(User, username=username).userprofile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = [
        'name',
        'address_line_1',
        'address_line_2',
        'address_city',
        'address_state',
        'address_code',
        'address_country',
    ]

    def get_object(self, **kwargs):
        return self.request.user.userprofile

class UserProfilePictureUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = [
        'profile_picture',
        'cropping',
    ]

    template_name = "exchange/userprofile_picture_form.html"

    def get_success_url(self):
        return reverse_lazy("edit_profile_picture")

    def get_object(self, **kwargs):
        return self.request.user.userprofile

class UserBookListView(LoginRequiredMixin, ListView):
    model = UserBook

    def get_queryset(self):
        self.username = self.kwargs['username'] if 'username' in self.kwargs else self.request.user.username
        self.user = get_object_or_404(User, username=self.username)
        return UserBook.objects.filter(owner=self.user).filter(holder=self.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserBookListView, self).get_context_data(**kwargs)
        context['userprofile'] = self.user.userprofile
        return context

@login_required
def book_add(request):
    if request.method == 'GET':
        return render(request, "exchange/book_add.html")
    else:
        google_id = request.POST['id']

        book, created = Book.objects.get_or_create(google_id)
        userbook = UserBook.objects.create(
                owner=request.user,
                holder=request.user,
                book=book)

        return redirect('your_books')


@login_required
def index(request):
    return render(request, 'exchange/index.html', {})



