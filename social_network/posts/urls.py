from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [path('<int:post_pk>/delete', views.delete_post, name='delete_post')
]