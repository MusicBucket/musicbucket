from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from bot import models as bot_models
from lastfm.models import LastfmUser
from spotify.models import Genre, Artist, Album, Track, SpotifyLink, SavedSpotifyLink, FollowedArtist
from telegram.models import TelegramUser, TelegramChat, SentSpotifyLink


class Command(BaseCommand):
    help = "Migrates the bot DB to the actual DB"

    def handle(self, *args, **options):
        self._migrate_telegram_users()
        self._migrate_telegram_chats()
        self._migrate_lastfm_users()
        self._migrate_genres()
        self._migrate_artists()
        self._migrate_albums()
        self._migrate_tracks()
        self._migrate_links()
        self._migrate_saved_links()
        self._migrate_followed_artists()
        self._clean_orphan_links()

    def _migrate_telegram_users(self):
        self.stdout.write('---------- Migrating telegram users')
        for bot_user in bot_models.User.objects.all():
            self.stdout.write(f'Migrating user {bot_user.username or bot_user.first_name}')
            user, was_created = TelegramUser.objects.get_or_create(
                telegram_id=bot_user.id,
                defaults={
                    'username': bot_user.username or '',
                    'first_name': bot_user.first_name or '',
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('---------- End migrating telegram users')

    def _migrate_telegram_chats(self):
        self.stdout.write('---------- Migrating telegram chats')
        for bot_chat in bot_models.Chat.objects.all():
            self.stdout.write(f'Migrating chat {bot_chat.name}')
            chat, was_created = TelegramChat.objects.get_or_create(
                telegram_id=bot_chat.id,
                defaults={
                    'name': bot_chat.name,
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('---------- End migrating telegram chats')

    def _migrate_lastfm_users(self):
        self.stdout.write('---------- Migrating telegram lastfm users')
        for bot_lastfm_user in bot_models.Lastfmusername.objects.all():
            lastfm_user, was_created = LastfmUser.objects.get_or_create(
                username=bot_lastfm_user.username,
                defaults={
                    'user': TelegramUser.objects.get(telegram_id=bot_lastfm_user.user.id)
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('---------- End migrating telegram lastfm users')

    def _migrate_genres(self):
        self.stdout.write('---------- Migrating telegram genres')
        for bot_genre in bot_models.Genre.objects.all():
            self.stdout.write(f'Migrating genre {bot_genre.name}')
            genre, was_created = Genre.objects.get_or_create(name=bot_genre.name)
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('---------- End migrating telegram genres')

    def _migrate_artists(self):
        self.stdout.write('---------- Migrating telegram artists')
        for bot_artist in bot_models.Artist.objects.all():
            self.stdout.write(f'Migrating artist {bot_artist.name}')
            artist, was_created = Artist.objects.get_or_create(
                spotify_id=bot_artist.id,
                defaults={
                    'name': bot_artist.name,
                    'href': bot_artist.href,
                    'url': bot_artist.spotify_url,
                    'uri': bot_artist.uri,
                    'popularity': bot_artist.popularity,
                    'image_url': bot_artist.image,
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('----- Migrating artist genres')
        for bot_artist_genre in bot_models.ArtistGenreThrough.objects.all():
            self.stdout.write(
                f'Migrating genre {bot_artist_genre.genre.name} for artist {bot_artist_genre.artist.name}'
            )
            artist = Artist.objects.get(spotify_id=bot_artist_genre.artist.id)
            artist.genres.add(Genre.objects.get(name=bot_artist_genre.genre.name))
        self.stdout.write('----- End Migrating artist genres')
        self.stdout.write('---------- End migrating telegram artists')

    def _migrate_albums(self):
        self.stdout.write('---------- Migrating telegram albums')
        for bot_album in bot_models.Album.objects.all():
            self.stdout.write(f'Migrating album {bot_album.name}')
            album, was_created = Album.objects.get_or_create(
                spotify_id=bot_album.id,
                defaults={
                    'name': bot_album.name,
                    'href': bot_album.href,
                    'url': bot_album.spotify_url,
                    'uri': bot_album.uri,
                    'popularity': bot_album.popularity,
                    'label': bot_album.label or '',
                    'image_url': bot_album.image,
                    'album_type': bot_album.album_type,
                    'release_date': bot_album.release_date,
                    'release_date_precision': bot_album.release_date_precision
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('----- Migrating album artists')
        for bot_album_artist in bot_models.AlbumArtistThrough.objects.all():
            self.stdout.write(
                f'Migrating artist {bot_album_artist.artist.name} for album {bot_album_artist.album.name}'
            )
            album = Album.objects.get(spotify_id=bot_album_artist.album.id)
            album.artists.add(Artist.objects.get(spotify_id=bot_album_artist.artist.id))
        self.stdout.write('----- End migrating album artists')
        self.stdout.write('----- Migrating album genres')
        for bot_album_genre in bot_models.AlbumGenreThrough.objects.all():
            self.stdout.write(
                f'Migrating genre {bot_album_genre.genre.name} for album {bot_album_genre.album.name}'
            )
            album = Album.objects.get(spotify_id=bot_album_genre.album.id)
            album.genres.add(Genre.objects.get(name=bot_album_genre.genre.name))
        self.stdout.write('----- End migrating album genres')
        self.stdout.write('---------- End migrating telegram albums')

    def _migrate_tracks(self):
        self.stdout.write('---------- Migrating telegram tracks')
        for bot_track in bot_models.Track.objects.all():
            self.stdout.write(f'Migrating track {bot_track.name}')
            try:
                album = Album.objects.get(spotify_id=bot_track.album_id)
            except Album.DoesNotExist:
                self.stdout.write(f'WARNING: ALBUM NOT FOUND with Spotify ID {bot_track.album_id}')
                continue
            track, was_created = Track.objects.get_or_create(
                spotify_id=bot_track.id,
                defaults={
                    'name': bot_track.name,
                    'href': bot_track.href,
                    'url': bot_track.spotify_url,
                    'uri': bot_track.uri,
                    'popularity': bot_track.popularity,
                    'number': bot_track.track_number,
                    'duration': bot_track.duration_ms,
                    'explicit': bot_track.explicit,
                    'preview_url': bot_track.preview_url or '',
                    'album': album
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('----- Migrating track artists')
        for bot_track_artist in bot_models.TrackArtistThrough.objects.all():
            self.stdout.write(
                f'Migrating artist {bot_track_artist.artist.name} for track {bot_track_artist.track.name}'
            )
            try:
                track = Track.objects.get(spotify_id=bot_track_artist.track.id)
                track.artists.add(Artist.objects.get(spotify_id=bot_track_artist.artist.id))
            except Track.DoesNotExist:
                pass
        self.stdout.write('----- End migrating track artists')
        self.stdout.write('---------- End migrating telegram tracks')

    def _migrate_links(self):
        self.stdout.write('---------- Migrating telegram tracks')
        for bot_link in bot_models.Link.objects.all():
            self.stdout.write(f'Migrating link {bot_link.url} of type {bot_link.link_type}')
            link_type = ''
            if bot_link.link_type == 'ARTIST':
                link_type = SpotifyLink.TYPE_ARTIST
            elif bot_link.link_type == 'ALBUM':
                link_type = SpotifyLink.TYPE_ALBUM
            elif bot_link.link_type == 'TRACK':
                link_type = SpotifyLink.TYPE_TRACK
            try:
                artist = Artist.objects.get(spotify_id=bot_link.artist_id)
            except Artist.DoesNotExist:
                artist = None
            try:
                album = Album.objects.get(spotify_id=bot_link.album_id)
            except Album.DoesNotExist:
                album = None
            try:
                track = Track.objects.get(spotify_id=bot_link.track_id)
            except Track.DoesNotExist:
                track = None
            link, was_created = SpotifyLink.objects.get_or_create(
                url=bot_link.url,
                defaults={
                    'link_type': link_type,
                    'artist': artist,
                    'album': album,
                    'track': track,
                }
            )
            if not was_created:
                self.stdout.write('Already created')
        self.stdout.write('----- Migrating link chats')
        for bot_chat_link in bot_models.Chatlink.objects.all():
            self.stdout.write(
                f'Migrating chat {bot_chat_link.chat.name} for link {bot_chat_link.link.url} of type {bot_chat_link.link.link_type}'
            )
            link = SpotifyLink.objects.get(url=bot_chat_link.link.url)
            SentSpotifyLink.objects.create(
                sent_at=make_aware(bot_chat_link.sent_at),
                sent_by=TelegramUser.objects.get(telegram_id=bot_chat_link.sent_by.id),
                chat=TelegramChat.objects.get(telegram_id=bot_chat_link.chat.id),
                link=link
            )
        self.stdout.write('----- End migrating link chats')
        self.stdout.write('---------- End migrating telegram tracks')

    def _migrate_saved_links(self):
        self.stdout.write('---------- Migrating saved links')
        for bot_saved_link in bot_models.Savedlink.objects.all():
            self.stdout.write(
                f'Migrating saved link {bot_saved_link.link.url} for user {bot_saved_link.user.username or bot_saved_link.user.first_name}'
            )
            SavedSpotifyLink.objects.create(
                user=TelegramUser.objects.get(telegram_id=bot_saved_link.user.id),
                link=SpotifyLink.objects.get(url=bot_saved_link.link.url),
                saved_at=make_aware(bot_saved_link.saved_at),
            )
        self.stdout.write('---------- End migrating saved links')

    def _migrate_followed_artists(self):
        self.stdout.write('---------- Migrating saved links')
        for bot_followed_artist in bot_models.Followedartist.objects.all():
            self.stdout.write(
                f'Migrating followed artist {bot_followed_artist.artist.name} for user {bot_followed_artist.user.username or bot_followed_artist.user.first_name}'
            )
            FollowedArtist.objects.create(
                user=TelegramUser.objects.get(telegram_id=bot_followed_artist.user.id),
                artist=Artist.objects.get(spotify_id=bot_followed_artist.artist.id),
                followed_at=make_aware(bot_followed_artist.followed_at),
                last_lookup=make_aware(bot_followed_artist.last_lookup),
            )
        self.stdout.write('---------- End migrating saved links')

    def _clean_orphan_links(self):
        self.stdout.write('---------- Cleaning orphan links')
        orphan_links_count = SpotifyLink.objects.all().count()
        for link in SpotifyLink.objects.all():
            if not link.link_type:
                self.stdout.write(f'Found orphan link: {link.url} (NO TYPE). Deleting.')
                link.delete()
            if link.link_type == SpotifyLink.TYPE_ARTIST and not link.artist:
                self.stdout.write(f'Found orphan link: {link.url} ({link.link_type}). Deleting.')
                link.delete()
            elif link.link_type == SpotifyLink.TYPE_ALBUM and not link.album:
                self.stdout.write(f'Found orphan link: {link.url} ({link.link_type}). Deleting.')
                link.delete()
            elif link.link_type == SpotifyLink.TYPE_TRACK and not link.track:
                self.stdout.write(f'Found orphan link: {link.url} ({link.link_type}). Deleting.')
                link.delete()
        self.stdout.write(f'---------- End cleaning orphan links. Deleted {orphan_links_count} links')
