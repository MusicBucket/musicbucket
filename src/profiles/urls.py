from django.contrib.auth import views as auth_views

from django.urls import path

app_name = 'profiles'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='profiles/login.html'),
        name="login",
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]
