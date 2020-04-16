from django import template
from django.conf import settings
from django.template.defaultfilters import safe
from django_telegram_login.widgets.constants import MEDIUM
from django_telegram_login.widgets.generator import create_redirect_login_widget

register = template.Library()


@register.simple_tag
def telegram_login_button() -> str:
    telegram_login_widget = create_redirect_login_widget(bot_name=settings.TELEGRAM_BOT_NAME,
                                                         redirect_url=settings.TELEGRAM_LOGIN_REDIRECT_URL,
                                                         size=MEDIUM)
    return safe(telegram_login_widget)
