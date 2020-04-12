from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2 import TemplateColumn

from telegram.models import SentSpotifyLink

default_attrs = {'class': 'table'}


class SentSpotifyLinkTable(tables.Table):
    cover = TemplateColumn(
        template_name='telegram/tables/sent_spotify_links_cover_column.html', orderable=False
    )
    link = TemplateColumn(
        verbose_name=_('Link'), template_name='telegram/tables/sent_spotify_links_link_column.html', orderable=False
    )
    spotify_url = TemplateColumn(
        verbose_name=_('Spotify'), template_name='telegram/tables/sent_spotify_links_spotify_url_column.html',
        orderable=False
    )
    link__link_type = TemplateColumn(
        template_name='telegram/tables/sent_spotify_links_link_type_column.html',
    )

    class Meta:
        model = SentSpotifyLink
        attrs = default_attrs
        fields = ('cover', 'link', 'spotify_url', 'link__link_type', 'chat__name', 'sent_by__username', 'sent_at')
        empty_text = _('There are not Sent Spotify Links in this chat')
