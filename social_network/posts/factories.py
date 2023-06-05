import factory
from django.contrib.auth import get_user_model
from faker import Factory
from core.models import Profile

from posts import models

factory_ru = Factory.create('ru-Ru')


class Post(factory.django.DjangoModelFactory):
    user = factory.SubFactory(get_user_model())
    profile = factory.SubFactory(Profile)
    to_user = factory.SubFactory(get_user_model())
    content = factory_ru.text(max_nb_chars=30)
    category = factory.SubFactory(models.Category)

    class Meta:
        model = models.Posts


class Category(factory.django.DjangoModelFactory):
    name = factory_ru.name()

    class Meta:
        model = models.Category


class Comment(factory.django.DjangoModelFactory):
    user = factory.SubFactory(get_user_model())
    profile = factory.SubFactory(Profile)
    post = factory.SubFactory(models.Posts)
    comment = factory_ru.text(max_nb_chars=30)

    class Meta:
        model = models.Comments
