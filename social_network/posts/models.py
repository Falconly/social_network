from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from django.db import models
from django.shortcuts import get_object_or_404


# Create your models here.
class PostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def posts(self, user):
        posts = list(Posts.objects.select_related('to_user').filter(to_user=user))
        return posts

    def post(self, pk_post):
        post = get_object_or_404(Posts, pk=pk_post)
        return post


class Posts(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь', blank=True)
    profile = models.ForeignKey('core.profile', on_delete=models.CASCADE, verbose_name='Профиль', blank=True)
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Получатель поста', blank=True,
                                related_name='+')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_modified = models.DateTimeField('Дата обновления', blank=True, null=True)
    image = models.ImageField('Фотография поста', blank=True, null=True,
                              upload_to='posts/%Y/%m/%d',
                              validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))])
    content = models.TextField('Содержание', max_length=255)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT)

    objects = PostsManager()

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        db_table = 'app_posts'

    @property
    def get_photo(self):
        return self.image.url

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


class Comments(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь', blank=True)
    profile = models.ForeignKey('core.profile', on_delete=models.CASCADE, verbose_name='Профиль', blank=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Пост', blank=True, related_name='comments')
    comment = models.TextField('Комментарий', max_length=255)
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_modified = models.DateTimeField('Дата редактирования', blank=True, null=True)

    class Meta:
        ordering = ('date_created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий #{self.pk}'
