from rest_framework import serializers

from api.modules.spotify.serializers import AlbumSerializer, ArtistSerializer


class MostSentArtistsSerializer(serializers.Serializer):
    sent_count = serializers.IntegerField()
    artist = ArtistSerializer(many=False)

    class Meta:
        fields = "__all__"

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass


class StatsSerializer(serializers.Serializer):
    artists_count = serializers.IntegerField()
    albums_count = serializers.IntegerField()
    tracks_count = serializers.IntegerField()
    sent_spotify_links_count = serializers.IntegerField()
    telegram_users_count = serializers.IntegerField()
    telegram_chats_count = serializers.IntegerField()
    most_sent_artists = MostSentArtistsSerializer(many=True)
    last_sent_albums = AlbumSerializer(many=True)

    class Meta:
        fields = [
            "artists_count",
            "albums_count",
            "tracks_count",
            "sent_spotify_links_count",
            "telegram_users_count",
            "telegram_chats_count",
            "most_sent_artists",
            "last_sent_albums",
        ]

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass
