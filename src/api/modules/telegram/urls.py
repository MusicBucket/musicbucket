from django.urls import path
from api.modules.telegram import views

urlpatterns = [
    path(
        'users/',
        views.TelegramUserListCreateAPIView.as_view(),
        name='user-list-create')
    ,
    path(
        'users/<str:telegram_id>/',
        views.TelegramUserRetrieveUpdateDestroyAPIView.as_view(),
        name='user-retrieve-update-destroy'
    ),
    path(
        'chats/',
        views.TelegramChatListCreateAPIView.as_view(),
        name='chat-list-create'
    ),
    path(
        'chats/<str:telegram_id>/',
        views.TelegramChatRetrieveUpdateDestroyAPIView.as_view(),
        name='chat-retrieve-update-destroy'
    ),
    path(
        'sent-spotify-links/',
        views.SentSpotifyLinksListCreateAPIView.as_view(),
        name='sent-spotify-link-list-create'
    ),
    path(
        'stats/<str:chat__telegram_id>/',
        views.StatsAPIView.as_view(),
        name='stats'
    ),

]
