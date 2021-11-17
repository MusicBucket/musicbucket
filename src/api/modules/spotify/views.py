import datetime
from typing import Dict

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response

from api.modules.spotify.filters import SavedSpotifyLinkFilter, FollowedArtistFilter
from api.modules.spotify.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, SpotifyLinkSerializer, \
    SavedSpotifyLinkSerializer, FollowedArtistSerializer, SearchResultSerializer, SpotifyRegisterSerializer
from profiles.models import Profile
from spotify.client import SpotifyClient
from spotify.models import Artist, Track, Album, SpotifyLink, SavedSpotifyLink, FollowedArtist, SpotifyTokensSet, \
    SpotifyUser


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


@authentication_classes([])
@permission_classes([])
class AuthURLView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Refactor this
        scopes = 'user-read-private user-read-email user-library-read user-read-currently-playing user-read-playback-state user-read-recently-played user-top-read'
        url = requests.Request("GET", "https://accounts.spotify.com/authorize", params={
            "scope": scopes,
            "response_type": "code",
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
        }).prepare().url

        return Response({"url": url}, status=status.HTTP_200_OK)


@authentication_classes([])
@permission_classes([])
class AuthCallbackView(generics.GenericAPIView):
    """
    Dummy View for Spotify OAuth for Callback URL.
    """

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


@authentication_classes([])
@permission_classes([])
class RegisterView(generics.GenericAPIView):
    serializer_class = SpotifyRegisterSerializer

    def post(self, request, *args, **kwargs):
        request = request.data
        access_token = request["access_token"]
        refresh_token = request["refresh_token"]
        token_type = request["token_type"]
        expires_in = request["expires_in"]
        # scope = request["scope"]

        if not access_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        spotify_user_data = self._get_spotify_user_data(access_token)
        user = self._link_spotify_user_to_a_new_user_profile(spotify_user_data)

        if user:
            self._update_or_create_spotify_user_tokens(
                user.profile.spotify_user, access_token, token_type, expires_in, refresh_token
            )

        token, _ = Token.objects.get_or_create(user=user)

        #  TODO: May get return MusicBucket User info
        return Response({'token': token.key})

    @staticmethod
    def _get_spotify_user_data(access_token: str) -> Dict:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        return response.json()

    @staticmethod
    def _link_spotify_user_to_a_new_user_profile(spotify_user_data: Dict):
        spotify_user, _ = SpotifyUser.objects.update_or_create(
            spotify_id=spotify_user_data["id"],
            defaults={
                "display_name": spotify_user_data["display_name"],
                "email": spotify_user_data["email"],
                "country": spotify_user_data["country"],
                "href": spotify_user_data["href"],
                "url": spotify_user_data["external_urls"]["spotify"],
                "uri": spotify_user_data["uri"],
                "image_url": spotify_user_data["images"][0]["url"],
                "followers": spotify_user_data["followers"]["total"],
                "type": spotify_user_data["type"],
                "product": spotify_user_data["product"],
            })

        profile = spotify_user.profile
        if not profile:
            user_model = get_user_model()
            generated_password = user_model.objects.make_random_password()
            user, _ = user_model.objects.get_or_create(
                username=spotify_user_data["email"],
                defaults={
                    'email': spotify_user_data["email"],
                    'password': generated_password
                })
            profile, _ = Profile.objects.get_or_create(user_id=user.pk)
            spotify_user.profile = profile
            spotify_user.save(update_fields=['profile'])
            return user
        return profile.user

    @staticmethod
    def _update_or_create_spotify_user_tokens(user: SpotifyUser, access_token: str, token_type: str, expires_in: int,
                                              refresh_token: str):
        expires_in = datetime.datetime.utcfromtimestamp(expires_in / 1000)  # From ms (javascript) to s (python)
        tokens = None
        try:
            tokens = user.tokens
        except SpotifyTokensSet.DoesNotExist:
            pass

        if tokens:
            tokens.access_token = access_token
            tokens.refresh_token = refresh_token
            tokens.expires_in = expires_in
            tokens.token_type = token_type
            tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
        else:
            tokens = SpotifyTokensSet(
                user=user,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                token_type=token_type,
            )
            tokens.save()
        return tokens
