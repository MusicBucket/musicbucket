import django_tables2 as tables

from telegram.models import SentSpotifyLink


class SentSpotifyLinkTable(tables.Table):
    class Meta:
        model = SentSpotifyLink
