from django import template

from spotify.models import SpotifyLink

register = template.Library()


@register.simple_tag
def get_spotify_link_type_icon(spotify_link: SpotifyLink) -> str:
    if spotify_link.link_type == SpotifyLink.TYPE_ARTIST:
        return 'person'
    elif spotify_link.link_type == SpotifyLink.TYPE_ALBUM:
        return 'album'
    elif spotify_link.link_type == SpotifyLink.TYPE_TRACK:
        return 'music_note'
