from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path(r'auth', include('rest_framework.urls')),
    path(r'telegram/', include('api.modules.telegram.urls')),
    path(r'spotify/', include('api.modules.spotify.urls')),
    path(r'lastfm/', include('api.modules.lastfm.urls')),
    # path(r'profiles/', include('api.modules.profiles.urls')),
]
