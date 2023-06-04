from django.contrib.auth.views import LogoutView
from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [path('register/', views.RegisterUserView.as_view(), name='register'),
               path('', views.LoginUserView.as_view(), name='home'),
               path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),


               path('news/', views.ShowNewsView.as_view(), name='news'),

               path('profile/<slug:profile_slug>', views.ProfileView.as_view(), name="profile"),
               path('profile/<slug:profile_slug>/update', views.UpdateProfileView.as_view(), name="update_profile"),

               path('peoples/', views.PeoplesListView.as_view(), name="peoples"),

               path('profile/<slug:profile_slug>/follower', views.friendship_request, name="following"),
               path('profile/<slug:profile_slug>/friends', views.ShowFriendsView.as_view(), name="friends"),
               path('profile/<slug:profile_slug>/subs', views.ShowSubsView.as_view(), name="subs"),

               path('profile/<slug:profile_slug>/accept_friendship_request', views.friend_request_accept,
                    name="accept_friend"),
               path('profile/<slug:profile_slug>/reject', views.friend_request_reject, name="reject_friend"),
               path('profile/<slug:friend_slug>/delete_friend', views.delete_friend, name="delete_friend"),
               path('profile/<slug:profile_slug>/from_request', views.ShowFromRequestView.as_view(),
                    name="from_request"),
               path('profile/<slug:profile_slug>/rejected_requests', views.ShowRejectedRequestsView.as_view(),
                    name="rejected_requests"),
               path('profile/<slug:profile_slug>/your_rejected_requests', views.ShowYouRejectedRequestsView.as_view(),
                    name="your_rejected_requests"),
               path('profile/<slug:other_slug>/delete_request', views.friendship_request_delete, name="request_delete"),
               path('profile/<slug:other_slug>/repeat_request', views.friendship_request_repeat, name="repeat_request"),

               path('profile/<slug:other_slug>/block_user', views.block_user, name="block_user"),
               path('profile/<slug:profile_slug>/list_block_user', views.ShowBlockedUsersView.as_view(),
                    name="list_block_user"),
               path('profile/<slug:other_slug>/remove_block', views.remove_block, name="remove_block")
               ]
