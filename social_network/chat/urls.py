from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('create/<int:user_id>/', views.CreateChatView.as_view(), name='create_chat'),
    path('<int:chat_pk>/', views.ShowMessagesView.as_view(), name='messages'),
    path('', views.ListChatView.as_view(), name='chats'),
]