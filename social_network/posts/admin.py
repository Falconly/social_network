from django.contrib import admin
from posts import models

# Register your models here.
admin.site.register(models.Posts)
admin.site.register(models.Category)