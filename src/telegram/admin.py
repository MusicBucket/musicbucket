from django.contrib import admin

from lastfm.admin import LastfmUserInline
from telegram.models import TelegramUser, TelegramChat, SentSpotifyLink


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'link',)
    search_fields = ('username', 'first_name',)
    inlines = (LastfmUserInline,)


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_type',)
    list_filter = ('chat_type',)
    search_fields = ('name',)


@admin.register(SentSpotifyLink)
class SentSpotifyLinkAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sent_by', 'chat', 'sent_at']
    list_filter = ('link__link_type', 'chat',)
    search_fields = ('chat__name', 'sent_by__name', 'link__artist__name', 'link__album__name', 'link__track__name')
