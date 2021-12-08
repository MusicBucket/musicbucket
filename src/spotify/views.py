from django.urls import reverse_lazy
from django.views.generic import DeleteView

from spotify.models import SavedSpotifyLink


class SavedSpotifyLinkDeleteView(DeleteView):
    model = SavedSpotifyLink
    success_url = reverse_lazy("app:saved-spotify-link-list")
    # TODO: Add a message to messages framework to inform of the deletion
