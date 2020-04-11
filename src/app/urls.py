from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path(
        '',
        views.SentSpotifyLinkListView.as_view(),
        name='sent-spotify-link-list'
    ),
    path(
        r'<int:pk>/',
        views.SentSpotifyLinkListView.as_view(),
        name='sent-spotify-link-list'
    ),
]
