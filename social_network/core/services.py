from django.contrib.auth.models import User
from django.db.models import Q
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


def get_list_search_friend(user: User, user_name: str) -> List[User]:
    list_friends = Friend.objects.select_related("from_user").filter(
        Q(from_user__first_name__icontains=user_name, to_user=user) | Q(from_user__last_name__icontains=user_name,
                                                                        to_user=user))
    friends = [u.from_user for u in list_friends]
    return friends


def get_list_friend_request_input(request_user: User) -> List[FriendshipRequest]:
    friend_requests = list(FriendshipRequest.objects.select_related("from_user").filter(to_user=request_user))
    return friend_requests


def get_list_search_request_input(user: User, user_name: str) -> List[FriendshipRequest]:
    friend_requests = list(FriendshipRequest.objects.select_related("from_user").filter(
        Q(from_user__first_name__icontains=user_name, to_user=user) | Q(from_user__last_name__icontains=user_name,
                                                                        to_user=user)))
    return friend_requests


def get_remove_friend(request_user: User, other_user: User) -> bool:
    return Friend.objects.remove_friend(request_user, other_user)


def get_add_friend(request_user: User, other_user: User) -> FriendshipRequest:
    return Friend.objects.add_friend(request_user, other_user)


def get_sent_requests(request_user: User) -> List[FriendshipRequest]:
    return Friend.objects.sent_requests(user=request_user)


def get_search_sent_requests(user: User, user_name: str) -> List[FriendshipRequest]:
    qs = FriendshipRequest.objects.select_related("from_user", "to_user").filter(
        Q(to_user__first_name__icontains=user_name, from_user=user) | Q(to_user__last_name__icontains=user_name,
                                                                        from_user=user))
    return list(qs)


def get_rejected_requests(request_user: User) -> List[FriendshipRequest]:
    rejected_requests = FriendshipRequest.objects.select_related('to_user').filter(from_user=request_user)
    return list(rejected_requests)


def get_search_rejected_requests(user: User, user_name: str):
    rejected_requests = FriendshipRequest.objects.select_related('to_user').filter(
        Q(to_user__first_name__icontains=user_name, from_user=user) | Q(to_user__last_name__icontains=user_name,
                                                                        from_user=user))
    return rejected_requests


def get_you_rejected_requests(request_user: User) -> List[FriendshipRequest]:
    rejected_request = Friend.objects.rejected_requests(user=request_user)
    return rejected_request


def get_search_you_rejected_requests(user: User, user_name: str) -> List[FriendshipRequest]:
    qs = FriendshipRequest.objects.select_related(
        "from_user", "to_user"
    ).filter(Q(from_user__first_name__icontains=user_name, to_user=user, rejected__isnull=False) | Q(
        from_user__last_name__icontains=user_name,
        to_user=user, rejected__isnull=False))

    return list(qs)
