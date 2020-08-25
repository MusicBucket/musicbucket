from rest_framework import serializers

from api.modules.telegram.serializers import TelegramUserSerializer
from lastfm.models import LastfmUser


class LastfmUserSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = LastfmUser
        fields = '__all__'


class NowPlayingSerializer(serializers.Serializer):
    is_playing_now = serializers.BooleanField(read_only=True)
    lastfm_user = LastfmUserSerializer(allow_null=True, read_only=True)
    artist_name = serializers.CharField(allow_null=True, read_only=True)
    album_name = serializers.CharField(allow_null=True, read_only=True)
    track_name = serializers.CharField(allow_null=True, read_only=True)
    cover = serializers.URLField(allow_null=True, read_only=True)
    url_candidate = serializers.URLField(allow_null=True, read_only=True)

    class Meta:
        fields = ['is_playing_now', 'lastfm_user', 'artist_name', 'album_name', 'track_name', 'cover', 'url_candidate']

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass


class TopAlbumsSerializer(serializers.Serializer):
    lastfm_user = LastfmUserSerializer(allow_null=True, read_only=True)
    top_albums = serializers.ListField(read_only=True)

    class Meta:
        fields = ['lastfm_user', 'top_albums']

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass


class TopArtistsSerializer(serializers.Serializer):
    lastfm_user = LastfmUserSerializer(allow_null=True, read_only=True)
    top_artists = serializers.ListField(read_only=True)

    class Meta:
        fields = ['lastfm_user', 'top_artists']

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass


class TopTracksSerializer(serializers.Serializer):
    lastfm_user = LastfmUserSerializer(allow_null=True, read_only=True)
    top_tracks = serializers.ListField(read_only=True)

    class Meta:
        fields = ['lastfm_user', 'top_tracks']

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass
