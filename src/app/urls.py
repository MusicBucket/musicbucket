from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path(
        'sent-spotify-links/',
        views.SentSpotifyLinkListView.as_view(),
        name='sent-spotify-link-list'
    ),
    path(
        r'sent-spotify-links/<int:pk>/',
        views.SentSpotifyLinkDetailView.as_view(),
        name='sent-spotify-link-detail'
    ),
    path(
        'saved-spotify-links/',
        views.SavedSpotifyLinkListView.as_view(),
        name='saved-spotify-link-list'
    ),
    path(
        r'saved-spotify-links/<int:pk>/',
        views.SavedSpotifyLinkDetailView.as_view(),
        name='saved-spotify-link-detail'
    ),
    path(
        'followed-artists/',
        views.FollowedArtistListView.as_view(),
        name='followed-artist-list'
    ),
    path(
        r'followed_artists/<int:pk>/',
        views.FollowedArtistDetailView.as_view(),
        name='followed-artist-detail'
    ),
]
