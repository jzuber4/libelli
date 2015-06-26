from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import UserProfile

class UserProfileDetailView(DetailView):
    model = UserProfile

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username']).userprofile

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    fields = [
        'profile_picture',
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

user_profile_detail = login_required(UserProfileDetailView.as_view())
user_profile_update = login_required(UserProfileUpdateView.as_view())

@login_required
def index(request):
    return render(request, "exchange/index.html", {"hey": 0})

