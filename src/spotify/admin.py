from django.contrib import admin
from spotify.models import Genre, Artist, Album, Track, SpotifyLink, FollowedArtist, SavedSpotifyLink, SpotifyUser, \
    SpotifyTokensSet, PlayedTracksInfo, PlayedTrack


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'get_genres',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Genres'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'get_artists', 'get_genres',)
    search_fields = ('name', 'artist__name',)
    list_filter = ('album_type',)

    def get_artists(self, obj):
        return ", ".join([artist.name for artist in obj.artists.all()])

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_artists.short_description = 'Artists'
    get_genres.short_description = 'Genres'


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'album', 'get_artists', 'preview_url',)
    search_fields = ('name', 'album__name',)

    def get_artists(self, obj):
        return ", ".join([artist.name for artist in obj.artists.all()])

    get_artists.short_description = 'Artists'


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


class SpotifyTokensSetInline(admin.StackedInline):
    model = SpotifyTokensSet
    can_delete = False


@admin.register(SpotifyUser)
class SpotifyUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_name', 'email', 'get_profile_user_username',)
    search_fields = ('display_name', 'email',)
    inlines = [SpotifyTokensSetInline, ]

    def get_profile_user_username(self, obj):
        return obj.profile.user.username


@admin.register(SpotifyTokensSet)
class SpotifyTokensSetAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayedTracksInfo)
class PlayedTracksInfoAdmin(admin.ModelAdmin):
    list_display = ('get_user_display_name', 'updated_at')

    def get_user_display_name(self, obj):
        return obj.user.display_name


@admin.register(PlayedTrack)
class PlayedTrackAdmin(admin.ModelAdmin):
    list_display = ('played_tracks_info', 'track', 'played_at')
