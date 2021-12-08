from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from profiles.models import Profile
from spotify.models import SpotifyLink
from telegram.mixins import EmojiMixin


class BaseTelegramModel(models.Model):
    telegram_id = models.CharField(
        verbose_name=_("Telegram ID"), max_length=250, unique=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"), auto_now_add=True, null=True
    )

    class Meta:
        abstract = True


class TelegramUser(EmojiMixin, BaseTelegramModel):
    EMOJI = ":baby:"

    profile = models.OneToOneField(
        Profile,
        verbose_name=_("Profile"),
        related_name="telegram_user",
        null=True,
        on_delete=models.CASCADE,
    )
    username = models.CharField(verbose_name=_("Username"), max_length=250, blank=True)
    first_name = models.CharField(
        verbose_name=_("First name"), max_length=250, blank=True
    )
    link = models.URLField(
        verbose_name=_("URL"), max_length=250, blank=True, default=""
    )
    photo_url = models.URLField(
        verbose_name=_("Photo URL"), max_length=250, blank=True, default=""
    )

    @classmethod
    def get_chats(cls, pk):
        user_sent_links_chats_ids = SentSpotifyLink.objects.filter(
            sent_by_id=pk
        ).values_list("chat_id", flat=True)
        return TelegramChat.objects.filter(pk__in=user_sent_links_chats_ids)

    @classmethod
    def create_from_telegram_user(cls, telegram_user: {}):
        created_user = cls.objects.create(
            telegram_id=telegram_user.get("id"),
            username=telegram_user.get("username"),
            first_name=telegram_user.get("first_name"),
        )
        return created_user

    def __str__(self) -> str:
        return self.username or self.first_name


class TelegramChat(BaseTelegramModel):
    PRIVATE_TYPE = "private"
    CHANNEL_TYPE = "channel"
    GROUP_TYPE = "group"
    SUPERGROUP_TYPE = "supergroup"
    TYPES = (
        (PRIVATE_TYPE, _("Private")),
        (CHANNEL_TYPE, _("Channel")),
        (GROUP_TYPE, _("Group")),
        (SUPERGROUP_TYPE, _("Supergroup")),
    )
    name = models.CharField(verbose_name=_("Name"), max_length=250)
    chat_type = models.CharField(
        verbose_name=_("Type"), choices=TYPES, blank=True, default="", max_length=50
    )

    def __str__(self) -> str:
        return self.name


class SentSpotifyLink(models.Model):
    """Represents an Spotify Link in a determined chat"""

    sent_at = models.DateTimeField(verbose_name=_("Sent at"), default=timezone.now)
    sent_by = models.ForeignKey(
        TelegramUser,
        verbose_name=_("Sent by"),
        related_name="sent_links",
        on_delete=models.CASCADE,
    )
    chat = models.ForeignKey(
        TelegramChat,
        verbose_name=_("Chat"),
        related_name="sent_links",
        on_delete=models.CASCADE,
    )
    link = models.ForeignKey(
        SpotifyLink,
        verbose_name=_("Spotify Link"),
        related_name="sent_links",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Sent Spotify Link")
        verbose_name_plural = _("Sent Spotify Links")

    def __str__(self):
        return f"{self.link.url}. Sent by {self.sent_by.username or self.sent_by.first_name} ({self.sent_by.id}) at {self.chat.name} ({self.chat.id})"
