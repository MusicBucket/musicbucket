from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _


# Create your models here.
class Profile(models.Model):
    """Represents the user extra information"""
    user = models.OneToOneField(
        get_user_model(), verbose_name=_('User'), related_name='profile', on_delete=models.PROTECT
    )
