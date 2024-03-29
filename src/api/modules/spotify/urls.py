from django.urls import path
from api.modules.spotify import views

urlpatterns = [
    path(
        "artists/", views.ArtistListCreateAPIView.as_view(), name="artist-list-create"
    ),
    path(
        "artists/<str:spotify_id>/",
        views.ArtistRetrieveUpdateDestroyAPIView.as_view(),
        name="artist-retrieve-update-destroy",
    ),
    path(
        "albums/",
        views.AlbumListCreateAPIView.as_view(),
        name="album-list-create",
    ),
    path(
        "albums/<str:spotify_id>/",
        views.AlbumRetrieveUpdateDestroyAPIView.as_view(),
        name="album-retrieve-update-destroy",
    ),
    path(
        "tracks/",
        views.TrackListCreateAPIView.as_view(),
        name="track-list-create",
    ),
    path(
        "tracks/<str:spotify_id>",
        views.TrackRetrieveUpdateDestroyAPIView.as_view(),
        name="track-retrieve-update-destroy",
    ),
    path(
        "links/",
        views.SpotifyLinkCreateListView.as_view(),
        name="spotify-link-list-create",
    ),
    path(
        "links/<str:url>",
        views.SpotifyLinkRetrieveUpdateDestroyAPIView.as_view(),
        name="spotify-link-retrieve-update-destroy",
    ),
    path(
        "saved-links/",
        views.SavedSpotifyLinkCreateListView.as_view(),
        name="saved-spotify-link-list-create",
    ),
    path(
        "saved-links/<int:pk>/",
        views.SavedSpotifyLinkRetrieveUpdateDestroyAPIView.as_view(),
        name="saved-spotify-link-retrieve-update-destroy",
    ),
    path(
        "followed-artists/",
        views.FollowedArtistCreateListView.as_view(),
        name="followed-artist-link-list-create",
    ),
    path(
        "followed-artists/<int:pk>/",
        views.FollowedArtistRetrieveUpdateDestroyAPIView.as_view(),
        name="followed-artist-link-retrieve-update-destroy",
    ),
    path(
        "followed-artists/check-new-music-releases/",
        views.FollowedArtistCheckNewMusicReleases.as_view(),
        name="followed-artist-check-new-music-releases",
    ),
    path(
        "search/",
        views.SearchListAPIView.as_view(),
        name="search",
    ),
    path("get-auth-url/", views.AuthURLView.as_view(), name="auth"),
    path("auth-callback/", views.AuthCallbackView.as_view(), name="auth-callback"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
