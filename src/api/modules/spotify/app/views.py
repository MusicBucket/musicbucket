import datetime
from typing import Dict

import django_rq
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.modules.spotify.serializers import (
    SpotifyRegisterSerializer,
    PlayedTrackSerializer,
)
from profiles.models import Profile
from spotify.models import (
    SpotifyTokensSet,
    SpotifyUser,
)
from spotify.services.updater import SpotifyUpdater


# TODO: Extract to pagination.py
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RecentlyPlayed(generics.ListAPIView):
    serializer_class = PlayedTrackSerializer
    pagination_class = StandardResultsSetPagination

    # TODO: (Add django_filter?)

    def get_queryset(self):
        spotify_user = self.request.user.profile.spotify_user
        recently_played_tracks = (
            spotify_user.played_tracks_info.playedtrack_set.all()
                .prefetch_related("track", "track__album", "track__artists")
                .order_by("-played_at")
        )
        return recently_played_tracks


@authentication_classes([])
@permission_classes([])
class AuthURLView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Refactor this
        scopes = "user-read-private user-read-email user-library-read user-read-currently-playing user-read-playback-state user-read-recently-played user-top-read"
        url = (
            requests.Request(
                "GET",
                "https://accounts.spotify.com/authorize",
                params={
                    "scope": scopes,
                    "response_type": "code",
                    "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
                    "client_id": settings.SPOTIFY_CLIENT_ID,
                },
            )
                .prepare()
                .url
        )

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

        if not user:
            raise PermissionDenied()

        self._update_or_create_spotify_user_tokens(
            user.profile.spotify_user,
            access_token,
            token_type,
            expires_in,
            refresh_token,
        )
        self._update_spotify_user_data(user.profile.spotify_user)
        token, _ = Token.objects.get_or_create(user=user)

        #  TODO: May return MusicBucket User info
        token = TokenObtainPairSerializer.get_token(user=user)
        return Response({
            "access_token": str(token.access_token),
            "refresh_token": str(token),
        })

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
            },
        )

        profile = spotify_user.profile
        if not profile:
            user_model = get_user_model()
            generated_password = user_model.objects.make_random_password()
            user, _ = user_model.objects.get_or_create(
                username=spotify_user_data["email"],
                defaults={
                    "email": spotify_user_data["email"],
                    "password": generated_password,
                },
            )
            profile, _ = Profile.objects.get_or_create(user_id=user.pk)
            spotify_user.profile = profile
            spotify_user.save(update_fields=["profile"])
            return user
        return profile.user

    @staticmethod
    def _update_or_create_spotify_user_tokens(
            user: SpotifyUser,
            access_token: str,
            token_type: str,
            expires_in: int,
            refresh_token: str,
    ):
        expires_in = timezone.make_aware(datetime.datetime.utcfromtimestamp(expires_in))
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
            tokens.save(
                update_fields=[
                    "access_token",
                    "refresh_token",
                    "expires_in",
                    "token_type",
                ]
            )
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

    @staticmethod
    def _update_spotify_user_data(user: SpotifyUser):
        spotify_updater = SpotifyUpdater()
        django_rq.enqueue(spotify_updater.update, user)
