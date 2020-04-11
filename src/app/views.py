from django.views.generic import DetailView
from django_filters import views as filter_views
from django_tables2 import SingleTableMixin

from telegram.filters import SentSpotifyLinkFilter
from telegram.models import SentSpotifyLink
from telegram.tables import SentSpotifyLinkTable

DEFAULT_PAGINATE_BY = 20


class SentSpotifyLinkDetailView(DetailView):
    queryset = SentSpotifyLink.objects.all()
    template_name = 'app/sent_spotify_link/sent_spotify_link_detail.html'


class SentSpotifyLinkListView(SingleTableMixin, filter_views.FilterView):
    queryset = SentSpotifyLink.objects.select_related('link', 'link__artist', 'link__album', 'link__track', 'chat',
                                                      'sent_by').all().order_by('-sent_at')
    model = SentSpotifyLink
    template_name = 'app/sent_spotify_link/sent_spotify_link_list.html'
    table_class = SentSpotifyLinkTable
    filterset_class = SentSpotifyLinkFilter
    paginate_by = DEFAULT_PAGINATE_BY
