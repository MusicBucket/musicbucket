from django.urls import path

from spotify import views

app_name = 'spotify'

urlpatterns = [
    path(
        'saved-spotify-links/<int:pk>/delete/',
        views.SavedSpotifyLinkDeleteView.as_view(),
        name='saved-spotify-link-delete'
    )
]
