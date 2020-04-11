from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Represents the user extra information"""
    user = models.OneToOneField(
        get_user_model(), verbose_name=_('User'), related_name='profile', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'Profile: {self.user.username}'
