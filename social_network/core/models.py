from datetime import date, timedelta
from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from friendship.models import Friend, FriendshipRequest


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name="Профиль пользователя", on_delete=models.CASCADE)
    slug = models.SlugField("Персональная ссылка", unique=True, blank=True, max_length=255)
    bio = models.TextField("Информация о себе", max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        "Аватар пользователя",
        blank=True,
        upload_to="avatar/%Y/%m/%d",
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))])

    date_birthday = models.DateField("Дата рождения", blank=True, null=True)

    class Meta:
        ordering = ('user',)
        verbose_name = "Профиль"
        verbose_name_plural = 'Профили пользователей'
        db_table = 'app_profile'

    @property
    def get_avatar(self):
        """
        Получение аватара при отсутствии загруженного
        """
        if not self.avatar:
            return f'https://ui-avatars.com/api/?size=128&background=random&name={self.user.username}'
        return self.avatar.url

    @property
    def get_age(self):
        if self.date_birthday:
            return (date.today() - self.date_birthday) // timedelta(days=365.2425)
        return

    def get_absolute_url(self):
        return reverse('core:profile', kwargs={'profile_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        else:
            self.slug = self.slug.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


Friend._meta.verbose_name = 'Друзья'
Friend._meta.verbose_name_plural = 'Друзья'
Friend._meta.get_field('to_user').verbose_name = 'Для пользователя'
Friend._meta.get_field('from_user').verbose_name = 'От пользователя'
Friend._meta.get_field('created').verbose_name = 'Создан'

FriendshipRequest._meta.verbose_name = 'Запросы на дружбу'
FriendshipRequest._meta.verbose_name_plural = 'Запросы на дружбу'
FriendshipRequest._meta.get_field('to_user').verbose_name = 'Для пользователя'
FriendshipRequest._meta.get_field('from_user').verbose_name = 'От пользователя'
FriendshipRequest._meta.get_field('created').verbose_name = 'Создана'
FriendshipRequest._meta.get_field('rejected').verbose_name = 'Отклонена'
