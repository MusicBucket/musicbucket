from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2 import TemplateColumn

from spotify.models import SavedSpotifyLink, FollowedArtist
from telegram.models import SentSpotifyLink

default_attrs = {'class': 'table'}


class SavedSpotifyLinkTable(tables.Table):
    cover = TemplateColumn(
        template_name='spotify/tables/saved_spotify_links_cover_column.html', orderable=False
    )
    link = TemplateColumn(
        verbose_name=_('Link'), template_name='spotify/tables/saved_spotify_links_link_column.html', orderable=False
    )
    spotify_url = TemplateColumn(
        verbose_name=_('Spotify'), template_name='spotify/tables/saved_spotify_links_spotify_url_column.html',
        orderable=False
    )
    link__link_type = TemplateColumn(
        template_name='spotify/tables/saved_spotify_links_link_type_column.html',
    )

    # TODO: Add genres column

    class Meta:
        model = SavedSpotifyLink
        attrs = default_attrs
        fields = ('cover', 'link', 'spotify_url', 'link__link_type', 'user__username', 'saved_at')
        empty_text = _('There are not saved Spotify links in this chat')


class FollowedArtistTable(tables.Table):
    class Meta:
        model = FollowedArtist
        attrs = default_attrs
        fields = ('name',)
        empty_text = _('There are not followed artists')
