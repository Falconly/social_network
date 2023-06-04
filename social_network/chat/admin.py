from django.contrib import admin

from chat import models


# Register your models here.
class ChatAmin(admin.ModelAdmin):
    list_display = ('id', 'date_created')
    search_fields = ('id',)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'from_user', 'to_user', 'pub_date',)
    search_fields = ('id', 'chat', 'from_user', 'to_user')
    list_display_links = ('id', 'chat',)


admin.site.register(models.Chat, ChatAmin)
admin.site.register(models.Messages, MessagesAdmin)
