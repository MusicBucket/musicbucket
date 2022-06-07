from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views


app_name = "api"

urlpatterns = [
    path(
        "token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(r"telegram/", include("api.modules.telegram.urls")),
    path(r"spotify/", include("api.modules.spotify.urls")),
    path(r"lastfm/", include("api.modules.lastfm.urls")),
    path(r"web/", include("api.modules.web.urls")),
    # path(r'profiles/', include('api.modules.profiles.urls')),
]
