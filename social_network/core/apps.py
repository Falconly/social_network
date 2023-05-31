from django.apps import AppConfig
from friendship.apps import FriendshipConfig


class CoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Основа'

    def ready(self):
        import core.signals


FriendshipConfig.verbose_name = 'Дружеские отношения'
