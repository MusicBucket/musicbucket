from django.db import models

from django.utils.translation import gettext_lazy as _

from telegram.models import TelegramUser


class LastfmUser(models.Model):
    user = models.OneToOneField(
        TelegramUser,
        verbose_name=_("User"),
        related_name="lastfm_user",
        on_delete=models.CASCADE,
    )
    username = models.CharField(verbose_name=_("Username"), max_length=250, unique=True)

    def __str__(self):
        return f"Lastfm User {self.username}"
