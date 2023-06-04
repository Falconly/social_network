from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [path('<int:post_pk>/delete', views.delete_post, name='delete_post'),
               path('<int:post_pk>/update', views.UpdatePostView.as_view(), name='update_post'),

               path('<int:comment_pk>/delete_comment', views.delete_comment, name='delete_comment'),
               ]