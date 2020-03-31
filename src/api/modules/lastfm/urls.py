from django.urls import path
from api.modules.lastfm import views

urlpatterns = [
    path(
        'now-playing/<str:user__telegram_id>/',
        views.NowPlayingAPIView.as_view(),
        name='now-playing'
    ),
    path(
        'users/set-lastfm-user/<str:user__telegram_id>/',
        views.LastfmUserCreateUpdateAPIView.as_view(),
        name='user-retrieve-update-destroy'
    ),
]
