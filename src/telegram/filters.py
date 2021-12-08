from django.utils.translation import gettext_lazy as _

import django_filters

from telegram.models import SentSpotifyLink, TelegramUser


def get_user_chats_queryset(request):
    return TelegramUser.get_chats(request.user.profile.telegram_user.id)


class UserSentSpotifyLinkFilter(django_filters.FilterSet):
    chat = django_filters.ModelChoiceFilter(
        queryset=get_user_chats_queryset, empty_label=_("All")
    )
    sent_at_start_date = django_filters.DateFilter(
        field_name="sent_at", label=_("Sent at start date"), lookup_expr="gte"
    )
    sent_at_end_date = django_filters.DateFilter(
        field_name="sent_at", label=_("Sent at end date"), lookup_expr="lte"
    )

    # genres = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(), label=_('Genres'))

    # TODO: Add genres filter

    class Meta:
        model = SentSpotifyLink
        fields = [
            "link__link_type",
            "chat",
            "sent_at_start_date",
            "sent_at_end_date",
        ]
