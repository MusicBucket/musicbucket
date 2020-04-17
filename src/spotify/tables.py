from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2 import TemplateColumn

from spotify.models import SavedSpotifyLink, FollowedArtist

default_attrs = {'class': 'table responsive-table'}


class SavedSpotifyLinkTable(tables.Table):
    cover = TemplateColumn(
        template_name='app/saved_spotify_link/tables/saved_spotify_links_cover_column.html', orderable=False
    )
    link = TemplateColumn(
        verbose_name=_('Link'), template_name='app/saved_spotify_link/tables/saved_spotify_links_link_column.html',
        orderable=False
    )
    spotify_url = TemplateColumn(
        verbose_name=_('Spotify'),
        template_name='app/saved_spotify_link/tables/saved_spotify_links_spotify_url_column.html',
        orderable=False
    )
    link__link_type = TemplateColumn(
        template_name='app/saved_spotify_link/tables/saved_spotify_links_link_type_column.html',
    )
    genres = TemplateColumn(
        template_name='app/saved_spotify_link/tables/saved_spotify_links_genres_column.html', orderable=False,
    )
    actions = TemplateColumn(
        template_name='app/saved_spotify_link/tables/saved_spotify_links_actions_column.html', orderable=False,
    )

    class Meta:
        model = SavedSpotifyLink
        attrs = default_attrs
        fields = ('cover', 'link', 'genres', 'spotify_url', 'link__link_type', 'saved_at')
        empty_text = _('There are not saved Spotify links in this chat')


class FollowedArtistTable(tables.Table):
    photo = TemplateColumn(
        template_name='app/followed_artist/tables/followed_artist_photo_column.html', orderable=False,
    )
    genres = TemplateColumn(
        template_name='app/followed_artist/tables/followed_artist_genres_column.html', orderable=False,
    )
    # TODO: New Music notification column
    # notification = TemplateColumn(
    #   template_name = 'app/followed_artist/tables/followed_artist_notification_column.html',
    # )

    class Meta:
        model = FollowedArtist
        attrs = default_attrs
        fields = ('photo', 'artist__name', 'genres')
        empty_text = _('There are not followed artists')
