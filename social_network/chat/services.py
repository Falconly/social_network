from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q, Count, QuerySet

from typing import List

from chat import models


def get_messages_list(from_user: User, to_user: User) -> QuerySet(models.Messages):
    return models.Messages.objects.filter(
        (Q(from_user=from_user) & Q(to_user=to_user) | (Q(from_user=to_user) & Q(to_user=from_user))))


def get_to_user(chat: models.Chat, request_user_pk: int) -> User:
    return chat.members.get(~Q(pk=request_user_pk))


def get_user(user_pk: int) -> User:
    return get_user_model().objects.get(pk=user_pk)


def get_chats(request_user_pk: int, user_pk: int) -> QuerySet(models.Chat):
    chats = models.Chat.objects.filter(members__in=[request_user_pk, user_pk]).annotate(
        c=Count('members')).filter(c=2)
    return chats


def create_chat() -> models.Chat:
    return models.Chat.objects.create()


def get_chat(request_user: User) -> List[User]:
    qs = models.Chat.objects.filter(members__in=[request_user])
    return qs
