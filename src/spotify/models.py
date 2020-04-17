import datetime

from django.db import models, transaction
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from spotify.client import SpotifyClient
from telegram.mixins import EmojiMixin


class BaseSpotifyModel(models.Model):
    spotify_id = models.CharField(verbose_name=_('Spotify ID'), max_length=250, unique=True)
    name = models.CharField(verbose_name=_('Name'), max_length=250)
    href = models.URLField(verbose_name=_('Spotify API Href'), max_length=250, blank=True)
    url = models.URLField(verbose_name=_('Spotify URL'), max_length=250, blank=True)
    uri = models.CharField(verbose_name=_('URI'), max_length=250)
    popularity = models.IntegerField(verbose_name=_('Popularity'), blank=True, null=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=250, unique=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    @classmethod
    def get_or_create_from_spotify_genre(cls, spotify_genre: str):
        try:
            return cls.objects.get(name=spotify_genre)
        except cls.DoesNotExist:
            genre = cls.objects.create(name=spotify_genre)
            return genre

    def __str__(self) -> str:
        return self.name


class Artist(EmojiMixin, BaseSpotifyModel):
    EMOJI = ':busts_in_silhouette:'

    image_url = models.CharField(verbose_name=_('Image'), max_length=250, blank=True)
    genres = models.ManyToManyField(Genre, verbose_name=_('Genres'), related_name='artists')

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')

    @classmethod
    def get_or_create_from_spotify_artist(cls, spotify_artist: {}):
        try:
            return cls.objects.get(spotify_id=spotify_artist.get('id'))
        except cls.DoesNotExist:
            with transaction.atomic():
                image_url = spotify_artist['images'][0]['url'] if spotify_artist['images'] else ''
                artist = cls.objects.create(
                    spotify_id=spotify_artist.get('id'),
                    name=spotify_artist.get('name'),
                    image_url=image_url,
                    popularity=spotify_artist.get('popularity'),
                    href=spotify_artist.get('href'),
                    url=spotify_artist.get('external_urls').get('spotify'),
                    uri=spotify_artist.get('uri')
                )
                for spotify_genre in spotify_artist.get('genres'):
                    genre = Genre.get_or_create_from_spotify_genre(spotify_genre)
                    artist.genres.add(genre)
            return artist

    def __str__(self) -> str:
        return self.name


class Album(EmojiMixin, BaseSpotifyModel):
    EMOJI = ':cd:'

    TYPE_ALBUM = 'album'
    TYPE_SINGLE = 'single'
    TYPE_COMPILATION = 'compilation'
    TYPES = (
        (TYPE_ALBUM, _('Album')),
        (TYPE_SINGLE, _('Single')),
        (TYPE_COMPILATION, _('Compilation')),
    )
    RELEASE_DATE_PRECISION_DAY = 'day'
    RELEASE_DATE_PRECISION_MONTH = 'month'
    RELEASE_DATE_PRECISION_YEAR = 'year'
    RELEASE_DATE_PRECISIONS = (
        (RELEASE_DATE_PRECISION_DAY, _('Day')),
        (RELEASE_DATE_PRECISION_MONTH, _('Month')),
        (RELEASE_DATE_PRECISION_YEAR, _('Year')),
    )

    label = models.CharField(verbose_name=_('Label'), max_length=250, blank=True)
    image_url = models.CharField(verbose_name=_('Image'), max_length=250, blank=True)
    album_type = models.CharField(verbose_name=_('Type'), choices=TYPES, max_length=250)
    release_date = models.DateField(verbose_name=_('Release date'))
    release_date_precision = models.CharField(
        verbose_name=_('Release date precision'), choices=RELEASE_DATE_PRECISIONS, max_length=250
    )
    genres = models.ManyToManyField(Genre, verbose_name=_('Genres'), related_name='albums')
    artists = models.ManyToManyField(Artist, verbose_name=_('Artists'), related_name='albums')

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def get_first_artist(self) -> Artist:
        if self.artists.exists():
            return self.artists.first()

    def get_genres(self):
        return self.genres.all() or self.get_first_artist().genres.all()

    @classmethod
    def get_or_create_from_spotify_album(cls, spotify_album: {}):
        spotify_client = SpotifyClient()
        try:
            return cls.objects.get(spotify_id=spotify_album.get('id'))
        except cls.DoesNotExist:
            with transaction.atomic():
                image_url = spotify_album['images'][0]['url'] if spotify_album['images'] else ''
                album = cls.objects.create(
                    spotify_id=spotify_album.get('id'),
                    name=spotify_album.get('name'),
                    label=spotify_album.get('label'),
                    image_url=image_url,
                    popularity=spotify_album.get('popularity'),
                    href=spotify_album.get('href'),
                    url=spotify_album.get('external_urls').get('spotify'),
                    uri=spotify_album.get('uri'),
                    album_type=spotify_album.get('album_type'),
                    release_date=cls.parse_release_date(
                        spotify_album.get('release_date'), spotify_album.get('release_date_precision')
                    ),
                    release_date_precision=spotify_album.get('release_date_precision')
                )
                for spotify_artist_simplified in spotify_album.get('artists'):
                    artist_id = spotify_artist_simplified.get('id')
                    spotify_artist = spotify_client.client.artist(artist_id)
                    artist = Artist.get_or_create_from_spotify_artist(spotify_artist)
                    album.artists.add(artist)
                for spotify_genre in spotify_album.get('genres'):
                    genre = Genre.get_or_create_from_spotify_genre(spotify_genre)
                    album.genres.add(genre)
            return album

    @classmethod
    def parse_release_date(cls, release_date: str, release_date_precision) -> datetime.date:
        if release_date_precision == cls.RELEASE_DATE_PRECISION_DAY:
            return datetime.datetime.strptime(release_date, '%Y-%m-%d').date()
        elif release_date_precision == cls.RELEASE_DATE_PRECISION_MONTH:
            return datetime.datetime.strptime(release_date, '%Y-%m').date()
        elif release_date_precision == cls.RELEASE_DATE_PRECISION_YEAR:
            return datetime.datetime.strptime(release_date, '%Y').date()

    def __str__(self) -> str:
        return self.name


class Track(EmojiMixin, BaseSpotifyModel):
    EMOJI = ':musical_note:'

    number = models.PositiveIntegerField(verbose_name=_('Track number'), blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name=_('Duration (in ms)'), blank=True, null=True)
    explicit = models.BooleanField(verbose_name=_('Explicit'), blank=True, null=True)
    preview_url = models.URLField(verbose_name=_('Preview URL'), blank=True, max_length=250)
    album = models.ForeignKey(Album, verbose_name=_('Album'), related_name='tracks', on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist, verbose_name=_('Artists'), related_name='tracks')

    class Meta:
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')

    def get_first_artist(self) -> Artist:
        if self.artists.exists():
            return self.artists.first()

    @classmethod
    def get_or_create_from_spotify_track(cls, spotify_track: {}):
        try:
            return cls.objects.get(spotify_id=spotify_track.get('id'))
        except cls.DoesNotExist:
            with transaction.atomic():
                spotify_client = SpotifyClient()
                album_id = spotify_track.get('album').get('id')
                spotify_album = spotify_client.client.album(album_id)
                album = Album.get_or_create_from_spotify_album(spotify_album)
                track = cls.objects.create(
                    spotify_id=spotify_track.get('id'),
                    name=spotify_track.get('name'),
                    number=spotify_track.get('track_number'),
                    duration=spotify_track.get('duration_ms'),
                    explicit=spotify_track.get('explicit'),
                    popularity=spotify_track.get('popularity'),
                    href=spotify_track.get('href'),
                    url=spotify_track.get('external_urls').get('spotify'),
                    preview_url=spotify_track.get('preview_url') or '',
                    uri=spotify_track.get('uri'),
                    album=album,
                )
                for spotify_artist_simplified in spotify_track.get('artists'):
                    artist_id = spotify_artist_simplified.get('id')
                    spotify_artist = spotify_client.client.artist(artist_id)
                    artist = Artist.get_or_create_from_spotify_artist(spotify_artist)
                    track.artists.add(artist)
            return track

    def __str__(self) -> str:
        return self.name


class SpotifyLink(models.Model):
    """Represents a unique Spotify Link"""
    TYPE_ARTIST = 'artist'
    TYPE_ALBUM = 'album'
    TYPE_TRACK = 'track'
    TYPES = (
        (TYPE_ARTIST, _('Artist')),
        (TYPE_ALBUM, _('Album')),
        (TYPE_TRACK, _('Track')),
    )

    url = models.URLField(verbose_name=_('URL'), max_length=250, unique=True)
    link_type = models.CharField(verbose_name=_('Type'), choices=TYPES, max_length=250)
    artist = models.ForeignKey(
        Artist, verbose_name=_('Artist'), related_name='links', null=True, on_delete=models.PROTECT
    )
    album = models.ForeignKey(
        Album, verbose_name=_('Album'), related_name='links', null=True, on_delete=models.PROTECT
    )
    track = models.ForeignKey(
        Track, verbose_name=_('Track'), related_name='links', null=True, on_delete=models.PROTECT
    )
    chats = models.ManyToManyField(
        'telegram.TelegramChat', verbose_name=_('Chats'), related_name='links', through='telegram.SentSpotifyLink'
    )

    class Meta:
        verbose_name = _('Spotify Link')
        verbose_name_plural = _('Spotify Links')

    def __str__(self):
        return f'{self.url} ({self.link_type})'

    @property
    def name(self):
        if self.link_type == self.TYPE_ARTIST:
            return self.artist.name
        elif self.link_type == self.TYPE_ALBUM:
            return self.album.name
        elif self.link_type == self.TYPE_TRACK:
            return self.track.name

    @property
    def artist_name(self):
        if self.link_type == self.TYPE_ARTIST:
            return self.artist.name
        elif self.link_type == self.TYPE_ALBUM:
            return self.album.artists.first().name
        elif self.link_type == self.TYPE_TRACK:
            return self.track.artists.first().name

    @property
    def spotify_url(self):
        if self.link_type == self.TYPE_ARTIST:
            return self.artist.url
        elif self.link_type == self.TYPE_ALBUM:
            return self.album.url
        elif self.link_type == self.TYPE_TRACK:
            return self.track.url

    @property
    def image_url(self):
        if self.link_type == self.TYPE_ARTIST:
            return self.artist.image_url
        elif self.link_type == self.TYPE_ALBUM:
            return self.album.image_url
        elif self.link_type == self.TYPE_TRACK:
            return self.track.album.image_url

    @property
    def genres(self):
        if self.link_type == self.TYPE_ARTIST:
            return self.artist.genres.all()
        elif self.link_type == self.TYPE_ALBUM:
            return self.album.get_genres().all()
        elif self.link_type == self.TYPE_TRACK:
            return self.track.album.get_genres()

    @classmethod
    def get_or_create_from_spotify_url(cls, spotify_url: str):
        spotify_client = SpotifyClient()
        try:
            return cls.objects.get(url=spotify_url)
        except cls.DoesNotExist:
            entity_id = cls.get_entity_id_from_url(spotify_url)
            link_type = cls.get_link_type_from_url(spotify_url)
            spotify_link = cls(url=spotify_url)
            if link_type == cls.TYPE_ARTIST:
                uri = f'spotify:artist:{entity_id}'
                artist = spotify_client.client.artist(uri)
                spotify_link.link_type = cls.TYPE_ARTIST
                spotify_link.artist = Artist.get_or_create_from_spotify_artist(artist)
            elif link_type == cls.TYPE_ALBUM:
                uri = f'spotify:album:{entity_id}'
                album = spotify_client.client.album(uri)
                spotify_link.link_type = cls.TYPE_ALBUM
                spotify_link.album = Album.get_or_create_from_spotify_album(album)
            elif link_type == cls.TYPE_TRACK:
                uri = f'spotify:track:{entity_id}'
                track = spotify_client.client.track(uri)
                spotify_link.link_type = cls.TYPE_TRACK
                spotify_link.track = Track.get_or_create_from_spotify_track(track)
            spotify_link.save()
            return spotify_link

    @classmethod
    def get_link_type_from_url(cls, url):
        """Resolves the Spotify link type"""
        if 'artist' in url:
            return cls.TYPE_ARTIST
        elif 'album' in url:
            return cls.TYPE_ALBUM
        elif 'track' in url:
            return cls.TYPE_TRACK
        return None

    @staticmethod
    def get_entity_id_from_url(url):
        return url[url.rfind('/') + 1:]


class SavedSpotifyLink(models.Model):
    """Represents a Saved Spotify Link by an user in the Telegram Chat"""
    user = models.ForeignKey(
        'telegram.TelegramUser', verbose_name=_('User'), related_name='saved_links', on_delete=models.CASCADE
    )
    link = models.ForeignKey(SpotifyLink, verbose_name=_('Link'), related_name='saved_links', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(verbose_name=_('Saved at'), default=timezone.now)

    class Meta:
        verbose_name = _('Saved Spotify Link')
        verbose_name_plural = _('Saved Spotify Links')
        unique_together = ['user', 'link']

    def __str__(self):
        return f'{self.user.username or self.user.first_name} - {self.link.url}'


class FollowedArtist(models.Model):
    """Represents a followed artist by a Telegram User"""
    user = models.ForeignKey(
        'telegram.TelegramUser', verbose_name=_('User'), related_name='followed_artists', on_delete=models.CASCADE
    )
    artist = models.ForeignKey(Artist, verbose_name=_('Artist'), related_name='followed_by', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(verbose_name=_('Followed at'), default=timezone.now)
    last_lookup = models.DateTimeField(verbose_name=_('Last lookup'), blank=True, null=True)

    class Meta:
        verbose_name = _('Followed Artist')
        verbose_name_plural = _('Followed Artists')
        unique_together = ['user', 'artist']

    def __str__(self):
        return f'{self.artist.name} followed by {self.user.username or self.user.first_name} ({self.user_id})'
