import django_rq
from django.core.management import BaseCommand

from spotify.services.updater import SpotifyUpdater


class Command(BaseCommand):
    help = "Updates the recently played tracks for all the SpotifyUsers from the Spotify API"

    def handle(self, *args, **options):
        spotify_updater = SpotifyUpdater()
        django_rq.enqueue(spotify_updater.update)
