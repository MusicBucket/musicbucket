from django import template

from spotify.models import SpotifyLink, Artist

register = template.Library()


@register.simple_tag
def get_spotify_link_type_icon(spotify_link: SpotifyLink) -> str:
    if spotify_link.link_type == SpotifyLink.TYPE_ARTIST:
        return "person"
    elif spotify_link.link_type == SpotifyLink.TYPE_ALBUM:
        return "album"
    elif spotify_link.link_type == SpotifyLink.TYPE_TRACK:
        return "music_note"


@register.simple_tag
def get_link_first_genres_comma_separated(spotify_link: SpotifyLink) -> str:
    genres_num = 2
    return ", ".join(spotify_link.genres.values_list("name", flat=True)[:genres_num])


@register.simple_tag
def get_artist_first_genres_comma_separated(artist: Artist) -> str:
    genres_num = 2
    return ", ".join(artist.genres.values_list("name", flat=True)[:genres_num])
