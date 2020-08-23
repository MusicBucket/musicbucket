from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.modules.telegram.serializers import TelegramUserSerializer
from spotify.models import SpotifyLink, Artist, Album, Track, SavedSpotifyLink, FollowedArtist, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class ArtistSimplifiedSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Artist
        fields = ['id', 'spotify_id', 'name', 'href', 'url', 'uri', 'popularity', 'image_url', 'genres']


class AlbumSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    artists = ArtistSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'


class AlbumSimplifiedSerializer(serializers.ModelSerializer):
    artists = ArtistSimplifiedSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


class TrackSimplifiedSerializer(serializers.ModelSerializer):
    artists = ArtistSimplifiedSerializer(many=True)

    class Meta:
        model = Track
        fields = '__all__'


class SpotifyLinkSerializer(serializers.ModelSerializer):
    artist = ArtistSimplifiedSerializer(required=False)
    album = AlbumSimplifiedSerializer(required=False)
    track = TrackSimplifiedSerializer(required=False)

    class Meta:
        model = SpotifyLink
        fields = '__all__'


class SavedSpotifyLinkSerializer(serializers.ModelSerializer):
    # Read fields
    link = SpotifyLinkSerializer(read_only=True)
    user = TelegramUserSerializer(read_only=True)

    # Write fields
    link_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = SavedSpotifyLink
        fields = '__all__'

    def create(self, validated_data):
        """Because of unique together with link_id and user_id, we should validate if register already exists in DB"""
        try:
            return SpotifyLink.objects.get(
                link__id=validated_data.get('link_id'),
                user__id=validated_data.get('user_id')
            )
        except SavedSpotifyLink.DoesNotExist:
            return super().create(validated_data)


class FollowedArtistSerializer(serializers.ModelSerializer):
    # Read fields
    artist = ArtistSerializer(read_only=True)
    user = TelegramUserSerializer(read_only=True)

    # Write fields
    artist_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = FollowedArtist
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=FollowedArtist.objects.all(),
                fields=['artist_id', 'user_id']
            )
        ]


class SearchResultSerializer(serializers.Serializer):
    results = serializers.ListField()

    class Meta:
        fields = ['results']

    def create(self, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass

    def update(self, instance, validated_data):
        """UNUSED: This serializer is only used for querying operations"""
        pass
