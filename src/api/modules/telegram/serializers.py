from rest_framework import serializers

from api.modules.profiles.serializers import ProfileSerializer
from spotify.client import SpotifyClient
from spotify.models import SpotifyLink
from telegram.models import TelegramUser, TelegramChat, SentSpotifyLink


class TelegramUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    link = serializers.URLField(required=False)

    sent_links_chat__count = serializers.IntegerField(allow_null=True, read_only=True)

    class Meta:
        model = TelegramUser
        fields = ['id', 'profile', 'telegram_id', 'username', 'first_name', 'link', 'sent_links_chat__count']


class TelegramChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramChat
        fields = '__all__'


class SentSpotifyLinkSerializer(serializers.ModelSerializer):
    from api.modules.spotify.serializers import SpotifyLinkSerializer

    sent_by = TelegramUserSerializer(read_only=True)
    chat = TelegramChatSerializer(read_only=True)
    link = SpotifyLinkSerializer(read_only=True)
    spotify_preview_track = serializers.SerializerMethodField(read_only=True)

    url = serializers.URLField(write_only=True)
    chat_id = serializers.IntegerField(write_only=True)
    sent_by_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SentSpotifyLink
        fields = '__all__'

    def validate(self, attrs: {}) -> {}:
        validated_attrs = super().validate(attrs)
        self._ensure_spotify_link_exists(validated_attrs)
        return validated_attrs

    @staticmethod
    def _ensure_spotify_link_exists(validated_attrs):
        link_url = validated_attrs.pop('url')
        link = SpotifyLink.get_or_create_from_spotify_url(link_url)
        validated_attrs.update({'link_id': link.id})
        return link

    @staticmethod
    def get_spotify_preview_track(obj: SentSpotifyLink):
        spotify_client = SpotifyClient()
        if obj.link.link_type == SpotifyLink.TYPE_ARTIST:
            return spotify_client.get_artist_top_track(obj.link.artist)
        elif obj.link.link_type == SpotifyLink.TYPE_ALBUM:
            return spotify_client.get_album_first_track(obj.link.album)
        elif obj.link.link_type == SpotifyLink.TYPE_TRACK:
            return spotify_client.client.track(obj.link.track.spotify_id)


class StatsSerializer(serializers.Serializer):
    users_with_chat_link_count = TelegramUserSerializer(many=True)

    class Meta:
        fields = ['users_with_chat_link_count']

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass
