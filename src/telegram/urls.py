from django.urls import path
from telegram import views

app_name = 'telegram'

urlpatterns = [
    path(
        'login-callback/',
        views.TelegramLoginCallbackView.as_view(),
        name='login-callback'
    )
]
