from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from friendship.models import FriendshipRequest, Friend, Block
from typing import List

from core import models


def get_other_profile(slug: str) -> models.Profile:
    other_profile = get_object_or_404(models.Profile, slug=slug)
    return other_profile


def get_friend_request(request_user: User, other_user: User) -> FriendshipRequest | list:
    try:
        friend_request = FriendshipRequest.objects.select_related('from_user', 'to_user').get(
            from_user=request_user, to_user=other_user)
    except:
        return []
    return friend_request


def get_reverse_friend_request(request_user: User, other_user: User) -> FriendshipRequest | list:
    try:
        friend_request = FriendshipRequest.objects.select_related('to_user', 'from_user').get(from_user=other_user,
                                                                                              to_user=request_user
                                                                                              )
    except:
        return []
    return friend_request


def check_are_friends(request_user: User, other_user: User) -> bool:
    return Friend.objects.are_friends(request_user, other_user)


def get_list_friends(request_user: User) -> List[User]:
    list_friends = Friend.objects.friends(request_user)
    return list_friends


def get_list_friend_request_input(request_user: User) -> List[FriendshipRequest]:
    friend_requests = list(FriendshipRequest.objects.filter(to_user=request_user))
    return friend_requests


def get_remove_friend(request_user: User, other_user: User) -> bool:
    return Friend.objects.remove_friend(request_user, other_user)


def get_add_friend(request_user: User, other_user: User) -> FriendshipRequest:
    return Friend.objects.add_friend(request_user, other_user)


def get_sent_requests(request_user: User) -> FriendshipRequest:
    return Friend.objects.sent_requests(user=request_user)


def get_block_user(request_user: User, other_user: User):
    return Block.objects.add_block(request_user, other_user)


def get_blocked_users(request_user: User):
    return Block.objects.blocking(request_user)


def get_remove_block(request_user: User, other_user: User):
    return Block.objects.remove_block(request_user, other_user)
