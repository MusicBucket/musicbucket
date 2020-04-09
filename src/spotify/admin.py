from django.contrib import admin
from spotify.models import Genre, Artist, Album, Track, SpotifyLink, FollowedArtist, SavedSpotifyLink


# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(SpotifyLink)
class SpotifyLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'link_type', 'artist', 'album', 'track')
    list_filter = ('link_type',)


@admin.register(SavedSpotifyLink)
class SavedSpotifyLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(FollowedArtist)
class FollowedArtistAdmin(admin.ModelAdmin):
    pass
