from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Chat(models.Model):
    members = models.ManyToManyField(get_user_model(), verbose_name='Участники', related_name='chat')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Чат #{self.pk}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чат'
        ordering = ('-date_created',)


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='Чат', blank=True)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Отправитель', blank=True,
                                  related_name='messages'
                                  )
    to_user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='Получатель', blank=True,
                                related_name='+')
    pub_date = models.DateTimeField('Дата отправления', auto_now_add=True)
    date_modified = models.DateTimeField('Дата редактирования', blank=True, null=True)
    is_readed = models.BooleanField('Прочитано', default=False)
    text = models.TextField('Сообщение', max_length=255)

    def __str__(self):
        return f'{self.from_user} отправил сообщение {self.to_user} '

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
