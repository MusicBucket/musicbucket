from django_filters import rest_framework as filters

from spotify.models import SavedSpotifyLink, FollowedArtist


class SavedSpotifyLinkFilter(filters.FilterSet):
    user__telegram_id = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = SavedSpotifyLink
        fields = '__all__'


class FollowedArtistFilter(filters.FilterSet):
    user__telegram_id = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = FollowedArtist
        fields = '__all__'
