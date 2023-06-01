from django.contrib import admin
from friendship.admin import FriendshipRequestAdmin, FriendAdmin

from core import models


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user__username', 'slug')


FriendshipRequestAdmin.fields = ('from_user', 'to_user', 'created', 'rejected',)

admin.site.register(models.Profile, ProfileAdmin)
