from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path(r'auth', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path(r'telegram/', include('api.modules.telegram.urls')),
    path(r'spotify/', include('api.modules.spotify.urls')),
    path(r'lastfm/', include('api.modules.lastfm.urls')),
    path(r'web/', include('api.modules.web.urls')),
    # path(r'profiles/', include('api.modules.profiles.urls')),
]
