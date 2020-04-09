from django.contrib import admin

from lastfm.admin import LastfmUserInline
from telegram.models import TelegramUser, TelegramChat, SentSpotifyLink


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    inlines = [LastfmUserInline, ]


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    pass


@admin.register(SentSpotifyLink)
class SentSpotifyLinkAdmin(admin.ModelAdmin):
    list_filter = ('link__link_type',)
