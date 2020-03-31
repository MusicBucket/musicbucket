# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Album(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    popularity = models.BigIntegerField(blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    spotify_url = models.TextField(blank=True, null=True)
    album_type = models.TextField(blank=True, null=True)
    uri = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    release_date_precision = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'album'

    def __str__(self):
        return self.name


class AlbumArtistThrough(models.Model):
    id = models.BigAutoField(primary_key=True)
    album = models.ForeignKey(Album, models.DO_NOTHING, blank=True, null=True)
    artist = models.ForeignKey('Artist', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'album_artist_through'
        unique_together = (('album', 'artist'), ('album', 'artist'),)

    def __str__(self):
        return f'{self.artist.name} - {self.album.name}'


class AlbumGenreThrough(models.Model):
    id = models.BigAutoField(primary_key=True)
    album = models.ForeignKey(Album, models.DO_NOTHING, blank=True, null=True)
    genre = models.ForeignKey('Genre', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'album_genre_through'
        unique_together = (('album', 'genre'), ('album', 'genre'),)

    def __str__(self):
        return f'{self.album.name} ({self.genre.name})'


class Artist(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    popularity = models.BigIntegerField(blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    spotify_url = models.TextField(blank=True, null=True)
    uri = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist'


class ArtistGenreThrough(models.Model):
    id = models.BigAutoField(primary_key=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True)
    genre = models.ForeignKey('Genre', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_genre_through'
        unique_together = (('artist', 'genre'), ('artist', 'genre'),)

    def __str__(self):
        return f'{self.artist.name} ({self.genre.name})'


class Chat(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    playlist_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat'

    def __str__(self):
        return self.name


class Chatlink(models.Model):
    sent_at = models.DateTimeField()
    chat = models.ForeignKey(Chat, models.DO_NOTHING)
    link = models.ForeignKey('Link', models.DO_NOTHING)
    sent_by = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'chatlink'

    def __str__(self):
        return f'{self.chat.name} - {self.link.url}'


class Followedartist(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    artist = models.ForeignKey(Artist, models.DO_NOTHING)
    followed_at = models.DateTimeField()
    last_lookup = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'followedartist'

    def __str__(self):
        return f'{self.user.username or self.user.first_name} - {self.artist.name}'


class Genre(models.Model):
    name = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.name


class Lastfmusername(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    username = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lastfmusername'

    def __str__(self):
        return f'{self.user.username or self.user.first_name} - {self.username}'


class Link(models.Model):
    url = models.TextField()
    link_type = models.TextField(blank=True, null=True)
    streaming_service_type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    artist_name = models.TextField(blank=True, null=True)
    album_name = models.TextField(blank=True, null=True)
    track_name = models.TextField(blank=True, null=True)
    genre = models.TextField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    chat_id = models.TextField()
    last_update_user_id = models.TextField(blank=True, null=True)
    times_sent = models.BigIntegerField(blank=True, null=True)
    artist_id = models.TextField(blank=True, null=True)
    album_id = models.TextField(blank=True, null=True)
    track_id = models.TextField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'link'

    def __str__(self):
        return self.url


class Savedlink(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    link = models.ForeignKey(Link, models.DO_NOTHING)
    saved_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'savedlink'
        unique_together = (('user', 'link'),)

    def __str__(self):
        return f'{self.user.username or self.user.first_name} - {self.link.url}'


class Track(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    track_number = models.BigIntegerField(blank=True, null=True)
    duration_ms = models.BigIntegerField(blank=True, null=True)
    explicit = models.BooleanField(blank=True, null=True)
    popularity = models.BigIntegerField(blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    spotify_url = models.TextField(blank=True, null=True)
    preview_url = models.TextField(blank=True, null=True)
    uri = models.TextField(blank=True, null=True)
    album_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track'

    def __str__(self):
        return self.name


class TrackArtistThrough(models.Model):
    id = models.BigAutoField(primary_key=True)
    track = models.ForeignKey(Track, models.DO_NOTHING, blank=True, null=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track_artist_through'
        unique_together = (('track', 'artist'), ('track', 'artist'),)

    def __str__(self):
        return f'{self.artist.name} - {self.track.name}'


class User(models.Model):
    id = models.TextField(primary_key=True)
    username = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return f'{self.username or self.first_name} ({self.id})'
