from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from friendship.models import Friend, FriendshipRequest

from .models import UserProfile

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['friends'] = Friend.objects.friends(context['userprofile'].user)
        context['is_friend'] = self.request.user in context['friends']
        if not context['is_friend']:
            sent_request = FriendshipRequest.objects.filter(from_user=self.request.user, to_user=context['userprofile'].user)
            received_request = FriendshipRequest.objects.filter(from_user=context['userprofile'].user, to_user=self.request.user)
            if sent_request.exists():
                context['sent_request'] = sent_request[0]
            elif received_request.exists() and not received_request[0].rejected:
                context['received_request'] = received_request[0]
        return context

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username']).userprofile


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

@login_required
def index(request):
    return render(request, "exchange/index.html", {"hey": 0})

