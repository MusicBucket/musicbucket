import pylast
from PIL import Image
from django.conf import settings

from lastfmcollagegenerator.collage_generator import CollageGenerator


class LastfmClient:
    PERIODS = (
        pylast.PERIOD_7DAYS,
        pylast.PERIOD_1MONTH,
        pylast.PERIOD_3MONTHS,
        pylast.PERIOD_6MONTHS,
        pylast.PERIOD_12MONTHS,
        pylast.PERIOD_OVERALL
    )

    def __init__(self):
        self.network = pylast.LastFMNetwork(
            api_key=settings.LASTFM_API_KEY,
            api_secret=settings.LASTFM_API_SECRET
        )

    def now_playing(self, username: str) -> {}:
        try:
            track = self.network.get_user(username).get_now_playing()
            if not track:
                return
        except pylast.WSError:
            return

        album = track.get_album()

        try:
            cover = track.get_cover_image()
        except IndexError:
            cover = None

        data = {
            "artist": track.artist,
            "album": album,
            "track": track,
            "cover": cover
        }
        return data

    def check_if_user_exists(self, username: str) -> bool:
        self.network.get_user(username).get_name(properly_capitalized=True)
        return True

    def get_top_albums(self, username: str, period=pylast.PERIOD_7DAYS):
        top_albums = self.network.get_user(username).get_top_albums(period)
        return top_albums

    def get_top_artists(self, username: str, period=pylast.PERIOD_7DAYS):
        top_artists = self.network.get_user(username).get_top_artists(period)
        return top_artists

    def get_top_tracks(self, username: str, period=pylast.PERIOD_7DAYS):
        top_tracks = self.network.get_user(username).get_top_tracks(period)
        return top_tracks

    @staticmethod
    def generate_collage(
            username: str,
            cols: int,
            rows: int,
            entity: str = CollageGenerator.ENTITY_ALBUM,
            period: str = pylast.PERIOD_7DAYS
    ) -> Image:
        # TODO: This is a workaround method. CollageGenerator should
        #  instantiate KEY/SECRET by .env var by itself and keep those
        #  parameters optional. This way method wouldn't be necessary in
        #  collagegenerator/views.py.
        #  Otherwise move this method elsewhere
        collage_generator = CollageGenerator(
            lastfm_api_key=settings.LASTFM_API_KEY,
            lastfm_api_secret=settings.LASTFM_API_SECRET,
        )
        image = collage_generator.generate(
            entity, username, cols, rows, period
        )
        return image
