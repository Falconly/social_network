from django.contrib import admin
from posts import models


# Register your models here.
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user', 'post')


admin.site.register(models.Posts)
admin.site.register(models.Category)
admin.site.register(models.Comments, CommentsAdmin)