from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework import mixins as rf_mixins

from api.modules.lastfm.client import LastfmClient
from api.modules.lastfm.serializers import NowPlayingSerializer, LastfmUserSerializer
from lastfm.models import LastfmUser
from spotify.client import SpotifyClient
from spotify.models import SpotifyLink
from telegram.models import TelegramUser


class NowPlayingAPIView(generics.RetrieveAPIView):
    serializer_class = NowPlayingSerializer
    http_method_names = ['get']

    def get_object(self):
        telegram_user = get_object_or_404(TelegramUser, telegram_id=self.kwargs.get('user__telegram_id'))
        lastfm_user = telegram_user.lastfm_user
        lastfm_client = LastfmClient()

        now_playing_data = lastfm_client.now_playing(lastfm_user.username)

        data = {
            'is_playing_now': False,
            'lastfm_user': lastfm_user
        }
        if now_playing_data:
            data.update({
                'is_playing_now': True,
                'artist_name': now_playing_data.get('artist').name,
                'album_name': now_playing_data.get('album').title,
                'track_name': now_playing_data.get('track').title,
                'cover': now_playing_data.get('cover'),
                'url_candidate': self._search_for_candidate_spotify_url(now_playing_data)
            })
        return data

    @staticmethod
    def _search_for_candidate_spotify_url(now_playing_data: {}) -> str:
        spotify_client = SpotifyClient()
        album = now_playing_data.get('album')
        track = now_playing_data.get('track')

        if album:
            results = spotify_client.search_link(album, SpotifyLink.TYPE_ALBUM)
        else:
            results = spotify_client.search_link(track, SpotifyLink.TYPE_TRACK)
        if results:
            candidate_url = results[0]['external_urls']['spotify']
            return candidate_url


class LastfmUserCreateUpdateAPIView(rf_mixins.UpdateModelMixin, generics.CreateAPIView):
    """
    This view is slightly different from the others.
    It only allows to create a Last.fm User if it already exists.
    Otherwise, updates it.
    """
    serializer_class = LastfmUserSerializer
    lookup_field = 'user__telegram_id'

    def post(self, request, *args, **kwargs):
        user__telegram_id = self.kwargs.get('user__telegram_id')
        # Telegram user must exist first
        self._check_telegram_user_exists(user__telegram_id)
        if LastfmUser.objects.filter(user__telegram_id=user__telegram_id).exists():
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        lastfm_user = LastfmUser.objects.filter(user__telegram_id=self.kwargs.get('user__telegram_id'))
        return lastfm_user

    @staticmethod
    def _check_telegram_user_exists(user__telegram_id: str) -> TelegramUser:
        """
        Method that ensures that the requested TelegramUser exists
        before creating or updating the Lastfm registry
        """
        try:
            return TelegramUser.objects.get(telegram_id=user__telegram_id)
        except TelegramUser.DoesNotExist:
            raise PermissionDenied
