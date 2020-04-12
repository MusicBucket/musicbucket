from django.views.generic import DetailView, TemplateView, ListView
from django_filters import views as filter_views
from django_tables2 import SingleTableMixin

from spotify.models import SavedSpotifyLink, FollowedArtist
from spotify.tables import SavedSpotifyLinkTable, FollowedArtistTable
from telegram.filters import UserSentSpotifyLinkFilter
from telegram.models import SentSpotifyLink, TelegramUser
from telegram.tables import SentSpotifyLinkTable

DEFAULT_PAGINATE_BY = 20


class SentSpotifyLinkListView(SingleTableMixin, filter_views.FilterView):
    queryset = SentSpotifyLink.objects.all()
    model = SentSpotifyLink
    template_name = 'app/sent_spotify_link/sent_spotify_link_list.html'
    table_class = SentSpotifyLinkTable
    filterset_class = UserSentSpotifyLinkFilter
    paginate_by = DEFAULT_PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset \
            .select_related('link', 'link__artist', 'link__album', 'link__track', 'chat', 'sent_by') \
            .filter(chat__in=TelegramUser.get_chats(self.request.user.profile.telegram_user.id))
        return queryset.order_by('-sent_at')


class SentSpotifyLinkDetailView(DetailView):
    queryset = SentSpotifyLink.objects.all()
    template_name = 'app/sent_spotify_link/sent_spotify_link_detail.html'


class SavedSpotifyLinkListView(SingleTableMixin, ListView):
    queryset = SavedSpotifyLink.objects.all()
    model = SavedSpotifyLink
    template_name = 'app/saved_spotify_link/saved_spotify_link_list.html'
    table_class = SavedSpotifyLinkTable
    paginate_by = DEFAULT_PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('link', 'link__artist', 'link__album', 'link__track',
                                           'user').filter(user=self.request.user.profile.telegram_user)
        return queryset.order_by('-saved_at')


class SavedSpotifyLinkDetailView(DetailView):
    queryset = SavedSpotifyLink.objects.all()
    template_name = 'app/saved_spotify_link/saved_spotify_link_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.profile.telegram_user)


class FollowedArtistListView(SingleTableMixin, ListView):
    queryset = FollowedArtist.objects.all()
    model = FollowedArtist
    template_name = 'app/followed_artist/followed_artist_list.html'
    table_class = FollowedArtistTable
    paginate_by = DEFAULT_PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('artist', 'user').filter(user=self.request.user.profile.telegram_user)
        return queryset.order_by('-followed_at')


class FollowedArtistDetailView(DetailView):
    queryset = FollowedArtist.objects.all()
    template_name = 'app/followed_artist/followed_artist_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.profile.telegram_user)
