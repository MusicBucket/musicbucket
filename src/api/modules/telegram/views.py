from django.db.models import Sum, Count
from rest_framework import generics
from rest_framework import mixins as rf_mixins
from rest_framework.generics import get_object_or_404

from api.modules.telegram.filters import SentSpotifyLinkFilter
from api.modules.telegram.serializers import TelegramUserSerializer, TelegramChatSerializer, SentSpotifyLinkSerializer, \
    StatsSerializer
from telegram.models import TelegramUser, TelegramChat, SentSpotifyLink


class TelegramUserListCreateAPIView(rf_mixins.UpdateModelMixin, generics.ListCreateAPIView):
    """This view allows also to update a registry if it already exists"""
    serializer_class = TelegramUserSerializer
    pagination_class = None
    queryset = TelegramUser.objects.all()
    lookup_field = 'telegram_id'

    def post(self, request, *args, **kwargs):
        user_telegram_id = self.request.POST.get('telegram_id')
        if TelegramUser.objects.filter(telegram_id=user_telegram_id).exists():
            self.kwargs.update({'telegram_id': user_telegram_id})
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


class TelegramUserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()


class TelegramChatListCreateAPIView(rf_mixins.UpdateModelMixin, generics.ListCreateAPIView):
    """This view allows also to update a registry if it already exists"""
    serializer_class = TelegramChatSerializer
    pagination_class = None
    queryset = TelegramChat.objects.all()
    lookup_field = 'telegram_id'

    def post(self, request, *args, **kwargs):
        chat_telegram_id = self.request.POST.get('telegram_id')
        if TelegramChat.objects.filter(telegram_id=chat_telegram_id).exists():
            self.kwargs.update({'telegram_id': chat_telegram_id})
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


class TelegramChatRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TelegramChatSerializer
    queryset = TelegramChat.objects.all()


class SentSpotifyLinksListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SentSpotifyLinkSerializer
    filterset_class = SentSpotifyLinkFilter
    pagination_class = None
    queryset = SentSpotifyLink.objects.all().order_by('sent_at')


class StatsAPIView(generics.RetrieveAPIView):
    serializer_class = StatsSerializer
    http_method_names = ['get']

    def get_object(self):
        telegram_chat = get_object_or_404(TelegramChat, telegram_id=self.kwargs.get('chat__telegram_id'))
        users_with_chat_link_count = self._get_users_with_chat_link_count(telegram_chat)
        return {'users_with_chat_link_count': users_with_chat_link_count}

    @staticmethod
    def _get_users_with_chat_link_count(chat: TelegramChat):
        users_with_chat_link_count = TelegramUser.objects.filter(sent_links__chat=chat).annotate(sent_links_chat__count=Count('sent_links'))
        return users_with_chat_link_count


