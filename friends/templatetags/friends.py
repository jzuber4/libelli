from django import template
from friendship.models import FriendshipRequest, Friend

register = template.Library()

@register.assignment_tag
def get_unread_friend_request_count(user):
    return Friend.objects.unread_request_count(user=user)

@register.assignment_tag
def get_friends(user):
    return Friend.objects.friends(user=user)

