import django_filters

from telegram.models import SentSpotifyLink, TelegramChat, TelegramUser


class SentSpotifyLinkFilter(django_filters.FilterSet):
    chat = django_filters.ModelChoiceFilter(queryset=TelegramChat.objects.all(),
                                            empty_label="")  # TODO: Filter by user chats
    sent_by = django_filters.ModelChoiceFilter(queryset=TelegramUser.objects.all(), empty_label="")

    class Meta:
        model = SentSpotifyLink
        fields = ['sent_by', 'chat', ]
