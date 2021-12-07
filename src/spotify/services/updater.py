import datetime
import logging
import dateutil.parser
from typing import Dict, Tuple, List, Optional

import django_rq
from django.db.models import QuerySet
from django.utils import timezone

from spotify.client import SpotifyClient
from spotify.models import Track, SpotifyUser, PlayedTracksInfo, PlayedTrack

logger = logging.getLogger(__name__)


class SpotifyUpdater:
    UNTIL_1_MONTH_AGO_MS = (
        timezone.now() - datetime.timedelta(days=30)
    ).timestamp() * 1000

    def __init__(self):
        self.spotify_client = SpotifyClient()

    @django_rq.job
    def update(self, user=None):
        if not user:
            users, total_users = self._get_spotify_users()
        else:
            users, total_users = ([user], 1)
        for i, user in enumerate(users):
            counter = i + 1
            logger.info(
                f"-- Processing user: {user.display_name} ({user.id}). {counter} of {total_users}"
            )
            self.update_tokens(user)
            self._update_played_tracks(user)

    @staticmethod
    def _get_spotify_users() -> Tuple[QuerySet, QuerySet]:
        # TODO: This can be optimized filtering by user.played_tracks_info.updated_at
        qs = SpotifyUser.objects.all()
        return qs, qs.count()

    def update_tokens(self, user: SpotifyUser):
        logger.info("    -- Updating tokens...")
        tokens_response = self.spotify_client.refresh_token(user.tokens.refresh_token)
        user.tokens.expires_in = timezone.now() + datetime.timedelta(
            seconds=tokens_response["expires_in"]
        )
        user.tokens.token_type = tokens_response["token_type"]
        user.tokens.access_token = tokens_response["access_token"]
        user.tokens.save()
        logger.info("    - Tokens updated")

    def _update_played_tracks(self, user: SpotifyUser):
        played_tracks_info = self._get_or_create_users_played_track_info(user)
        logger.info(f"    -- Updating played tracks")
        # Check if this user already have synced any played track.
        # If not, it fills their played tracks from the beginning
        some_played_track = (
            PlayedTrack.objects.filter(played_tracks_info=played_tracks_info)
            .order_by("-played_at_ms")
            .first()
        )
        if some_played_track:
            self._sync_played_tracks(played_tracks_info, some_played_track)
        else:
            self._sync_played_tracks(played_tracks_info)

        played_tracks_info.updated_at = timezone.now()
        played_tracks_info.save()

    def _sync_played_tracks(
        self,
        played_tracks_info: PlayedTracksInfo,
        last_played_track: Optional[PlayedTrack] = None,
    ):
        cursor: int = int(timezone.now().timestamp() * 1000)
        if last_played_track:
            logger.info(
                f"    - Updating played tracks from: {datetime.datetime.utcfromtimestamp(cursor / 1000)}"
            )
            until = last_played_track.played_at_ms
        else:
            logger.info(
                f"    - Creating played tracks from scratch: {datetime.datetime.utcfromtimestamp(cursor / 1000)}"
            )
            until = self.UNTIL_1_MONTH_AGO_MS

        while cursor and cursor > until:
            response = self.spotify_client.get_users_recently_played_tracks(
                played_tracks_info.user, before_ms=cursor
            )
            newer_items = filter(
                lambda item: dateutil.parser.isoparse(item["played_at"]).timestamp()
                * 1000
                > until,
                response["items"],
            )
            played_tracks: List[PlayedTrack] = []
            for item in newer_items:
                played_tracks.append(
                    self._process_recently_played_item(item, played_tracks_info)
                )
            PlayedTrack.objects.bulk_create(played_tracks)
            new_cursor = (
                int(response["cursors"]["before"])
                if response["cursors"] is not None
                else None
            )
            logger.info(
                f"Created {len(played_tracks)} played tracks. "
                f"Cursor at: {datetime.datetime.utcfromtimestamp((new_cursor or cursor) / 1000)}"
            )
            cursor = new_cursor

    @staticmethod
    def _get_or_create_users_played_track_info(user: SpotifyUser) -> PlayedTracksInfo:
        logger.info("    -- Getting or creating users PlayedTrackInfo")
        played_tracks_info, created = PlayedTracksInfo.objects.get_or_create(user=user)
        if created:
            logger.info(f"    - Created PlayedTrackInfo: {played_tracks_info}")
        return played_tracks_info

    @staticmethod
    def _process_recently_played_item(item: Dict, played_tracks_info: PlayedTracksInfo):
        track = Track.get_or_create_from_spotify_track(item["track"])
        parsed_played_at = dateutil.parser.isoparse(item["played_at"])
        played_at = timezone.make_aware(timezone.make_naive(parsed_played_at))
        played_track = PlayedTrack(
            played_tracks_info=played_tracks_info,
            track=track,
            played_at=played_at,
            played_at_ms=parsed_played_at.timestamp() * 1000,
        )
        return played_track
