from django.conf import settings
from django.contrib.auth import views as auth_views
from django_telegram_login.widgets.constants import MEDIUM
from django_telegram_login.widgets.generator import create_redirect_login_widget


class LoginView(auth_views.LoginView):
    template_name = 'profiles/login.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data = self._define_telegram_login_button(context_data)
        return context_data

    @staticmethod
    def _define_telegram_login_button(context_data: {}) -> {}:
        telegram_login_widget = create_redirect_login_widget(bot_name=settings.TELEGRAM_BOT_NAME,
                                                             redirect_url=settings.TELEGRAM_LOGIN_REDIRECT_URL,
                                                             size=MEDIUM)
        context_data.update({'telegram_login_widget': telegram_login_widget})
        return context_data
