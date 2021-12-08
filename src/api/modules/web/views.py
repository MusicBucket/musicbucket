from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.modules.web.serializers import StatsSerializer
from spotify.models import Artist, Track, Album, SpotifyLink
from telegram.models import SentSpotifyLink, TelegramUser, TelegramChat


class StatsAPIView(generics.RetrieveAPIView):
    """Returns a JSON with few stats used by the Home page charts"""

    serializer_class = StatsSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get_object(self):
        stats = self._build_stats()
        return stats

    def _build_stats(self):
        stats = {
            "artists_count": self._get_artists_count(),
            "albums_count": self._get_albums_count(),
            "tracks_count": self._get_tracks_count(),
            "sent_spotify_links_count": self._get_sent_spotify_links_count(),
            "telegram_users_count": self._get_telegram_users_count(),
            "telegram_chats_count": self._get_telegram_chats_count(),
            "most_sent_artists": self._get_most_sent_artists(),
            "last_sent_albums": self._get_last_sent_albums(),
        }
        return stats

    @staticmethod
    def _get_most_sent_artists():
        most_sent_artists = (
            Artist.objects.all()
            .annotate(sent_count=Count("links__sent_links"))
            .order_by("-sent_count")
            .values()[:10]
        )
        most_sent_artists = [
            {
                "sent_count": artist.pop("sent_count"),
                "artist": artist,
            }
            for artist in most_sent_artists
        ]
        return most_sent_artists

    @staticmethod
    def _get_last_sent_albums():
        last_sent_albums = (
            Album.objects.filter(links__link_type=SpotifyLink.TYPE_ALBUM)
            .order_by("-links__sent_links__sent_at")
            .distinct()[:10]
        )
        return last_sent_albums

    @staticmethod
    def _get_artists_count():
        return Artist.objects.all().distinct().count()

    @staticmethod
    def _get_albums_count():
        return Album.objects.all().distinct().count()

    @staticmethod
    def _get_tracks_count():
        return Track.objects.all().distinct().count()

    @staticmethod
    def _get_sent_spotify_links_count():
        return SentSpotifyLink.objects.all().distinct().count()

    @staticmethod
    def _get_telegram_users_count():
        return TelegramUser.objects.all().distinct().count()

    @staticmethod
    def _get_telegram_chats_count():
        return TelegramChat.objects.all().distinct().count()
