from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework import generics

from api.modules.spotify.filters import SavedSpotifyLinkFilter, FollowedArtistFilter
from api.modules.spotify.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, SpotifyLinkSerializer, \
    SavedSpotifyLinkSerializer, FollowedArtistSerializer, SearchResultSerializer
from spotify.client import SpotifyClient
from spotify.models import Artist, Track, Album, SpotifyLink, SavedSpotifyLink, FollowedArtist


class ArtistListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ArtistSerializer
    pagination_class = None
    queryset = Artist.objects.all()


class ArtistRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    lookup_field = 'spotify_id'


class AlbumListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer
    pagination_class = None
    queryset = Album.objects.all()


class AlbumRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class TrackListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TrackSerializer
    pagination_class = None
    queryset = Track.objects.all()


class TrackRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class SpotifyLinkCreateListView(generics.ListCreateAPIView):
    serializer_class = SpotifyLinkSerializer
    pagination_class = None
    queryset = SpotifyLink.objects.all()


class SpotifyLinkRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpotifyLink.objects.all()


class SavedSpotifyLinkCreateListView(generics.ListCreateAPIView):
    serializer_class = SavedSpotifyLinkSerializer
    filterset_class = SavedSpotifyLinkFilter
    pagination_class = None
    queryset = SavedSpotifyLink.objects.all()


class SavedSpotifyLinkRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedSpotifyLinkSerializer
    queryset = SavedSpotifyLink.objects.all()


class FollowedArtistCreateListView(generics.ListCreateAPIView):
    serializer_class = FollowedArtistSerializer
    filterset_class = FollowedArtistFilter
    pagination_class = None
    queryset = FollowedArtist.objects.all()


class FollowedArtistRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FollowedArtistSerializer
    queryset = FollowedArtist.objects.all()


class FollowedArtistCheckNewMusicReleases(generics.ListAPIView):
    serializer_class = AlbumSerializer
    filterset_class = FollowedArtistFilter
    pagination_class = None
    queryset = FollowedArtist.objects.all()

    def filter_queryset(self, queryset):
        followed_artists_qs = super().filter_queryset(queryset)
        self._update_followed_artists_albums(followed_artists_qs)
        new_music_releases_qs = self._extract_new_music_releases(followed_artists_qs)
        self._update_followed_artists_last_lookup(followed_artists_qs)
        return new_music_releases_qs

    @staticmethod
    def _update_followed_artists_last_lookup(followed_artists_qs):
        for followed_artist in followed_artists_qs:
            followed_artist.last_lookup = timezone.now()
            followed_artist.save()

    @staticmethod
    def _update_followed_artists_albums(followed_artists_qs):
        spotify_client = SpotifyClient()
        for followed_artist in followed_artists_qs:
            spotify_artist_albums = spotify_client.get_all_artist_albums(followed_artist.artist)
            for spotify_album in spotify_artist_albums:
                Album.get_or_create_from_spotify_album(spotify_album)

    @staticmethod
    def _extract_new_music_releases(followed_artists_qs):
        new_albums_releases = Album.objects.prefetch_related('artists').filter(
            artists__in=followed_artists_qs.values_list('artist', flat=True),
            artists__followed_by__last_lookup__isnull=False,
            release_date__gte=F('artists__followed_by__last_lookup')
        )
        return new_albums_releases


class SearchListAPIView(generics.RetrieveAPIView):
    serializer_class = SearchResultSerializer
    http_method_names = ['get']

    def get_object(self):
        query = self.request.GET.get('query')
        entity_type = self.request.GET.get('entity_type')
        if not entity_type or not query:
            raise Http404
        search_results = self._search_links(query, entity_type)
        return {'results': search_results}

    @staticmethod
    def _search_links(query: str, entity_type: str):
        spotify_client = SpotifyClient()
        search_results = spotify_client.search_links(query, entity_type)
        return search_results
