from django.urls import path
from api.modules.lastfm import views

urlpatterns = [
    path(
        'now-playing/<str:user__telegram_id>/',
        views.NowPlayingAPIView.as_view(),
        name='now-playing'
    ),
    path(
        'users/<str:user__telegram_id>/top-albums/',
        views.TopAlbumsView.as_view(),
        name='top-albums'
    ),
    path(
        'users/<str:user__telegram_id>/top-artists/',
        views.TopArtistsView.as_view(),
        name='top-artists'
    ),
    path(
        'users/<str:user__telegram_id>/top-tracks/',
        views.TopTracksView.as_view(),
        name='top-tracks'
    ),
    path(
        'users/set-lastfm-user/',
        views.LastfmUserCreateUpdateAPIView.as_view(),
        name='user-retrieve-update-destroy'
    ),
]
