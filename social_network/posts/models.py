from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from pytils.translit import slugify


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Пользователь')
    profile = models.ForeignKey('core.profile', on_delete=models.PROTECT, verbose_name='Профиль', blank=True)
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_modified = models.DateTimeField('Дата обновления', auto_now_add=True)
    image = models.ImageField('Фотография поста', blank=True,
                              upload_to='posts/%Y/%m/%d',
                              validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))])
    content = models.TextField('Содержание', max_length=255)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT)

    class Meta:
        ordering = ('date_created',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        db_table = 'app_posts'

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Пост #{self.pk}"


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
