from django_filters import rest_framework as filters

from telegram.models import SentSpotifyLink


class TelegramUserFilter(filters.FilterSet):
    pass


class SentSpotifyLinkFilter(filters.FilterSet):
    chat__telegram_id = filters.CharFilter(lookup_expr='iexact')
    sent_by__telegram_id = filters.CharFilter(lookup_expr='iexact')
    sent_by__username = filters.CharFilter(lookup_expr='iexact')
    sent_at__gte = filters.DateFilter(field_name='sent_at', lookup_expr='gte')

    class Meta:
        model = SentSpotifyLink
        fields = [
            'sent_at', 'sent_by', 'chat__telegram_id', 'sent_by__telegram_id', 'sent_by__username', 'sent_at__gte'
        ]
