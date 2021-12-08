# Generated by Django 3.0.3 on 2020-03-31 14:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import telegram.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "spotify_id",
                    models.CharField(
                        max_length=250, unique=True, verbose_name="Spotify ID"
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "href",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Spotify API Href"
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Spotify URL"
                    ),
                ),
                ("uri", models.CharField(max_length=250, verbose_name="URI")),
                (
                    "popularity",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Popularity"
                    ),
                ),
                (
                    "label",
                    models.CharField(blank=True, max_length=250, verbose_name="Label"),
                ),
                (
                    "image_url",
                    models.CharField(blank=True, max_length=250, verbose_name="Image"),
                ),
                (
                    "album_type",
                    models.CharField(
                        choices=[
                            ("album", "Album"),
                            ("single", "Single"),
                            ("compilation", "Compilation"),
                        ],
                        max_length=250,
                        verbose_name="Type",
                    ),
                ),
                ("release_date", models.DateField(verbose_name="Release date")),
                (
                    "release_date_precision",
                    models.CharField(
                        choices=[("day", "Day"), ("month", "Month"), ("year", "Year")],
                        max_length=250,
                        verbose_name="Release date precision",
                    ),
                ),
            ],
            options={
                "verbose_name": "Album",
                "verbose_name_plural": "Albums",
            },
            bases=(telegram.mixins.EmojiMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "spotify_id",
                    models.CharField(
                        max_length=250, unique=True, verbose_name="Spotify ID"
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "href",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Spotify API Href"
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Spotify URL"
                    ),
                ),
                ("uri", models.CharField(max_length=250, verbose_name="URI")),
                (
                    "popularity",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Popularity"
                    ),
                ),
                (
                    "image_url",
                    models.CharField(blank=True, max_length=250, verbose_name="Image"),
                ),
            ],
            options={
                "verbose_name": "Artist",
                "verbose_name_plural": "Artists",
            },
            bases=(telegram.mixins.EmojiMixin, models.Model),
        ),
        migrations.CreateModel(
            name="FollowedArtist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "followed_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Followed at"
                    ),
                ),
                (
                    "last_lookup",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Last lookup"
                    ),
                ),
            ],
            options={
                "verbose_name": "Followed Artist",
                "verbose_name_plural": "Followed Artists",
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=250, unique=True, verbose_name="Name"),
                ),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
            },
        ),
        migrations.CreateModel(
            name="SavedSpotifyLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "saved_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Saved at"
                    ),
                ),
            ],
            options={
                "verbose_name": "Saved Spotify Link",
                "verbose_name_plural": "Saved Spotify Links",
            },
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "spotify_id",
                    models.CharField(
                        max_length=250, unique=True, verbose_name="Spotify ID"
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "href",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Spotify API Href"
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Spotify URL"
                    ),
                ),
                ("uri", models.CharField(max_length=250, verbose_name="URI")),
                (
                    "popularity",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Popularity"
                    ),
                ),
                (
                    "number",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Track number"
                    ),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Duration (in ms)"
                    ),
                ),
                (
                    "explicit",
                    models.BooleanField(blank=True, null=True, verbose_name="Explicit"),
                ),
                (
                    "preview_url",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Preview URL"
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracks",
                        to="spotify.Album",
                        verbose_name="Album",
                    ),
                ),
                (
                    "artists",
                    models.ManyToManyField(
                        related_name="tracks",
                        to="spotify.Artist",
                        verbose_name="Artists",
                    ),
                ),
            ],
            options={
                "verbose_name": "Track",
                "verbose_name_plural": "Tracks",
            },
            bases=(telegram.mixins.EmojiMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SpotifyLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "url",
                    models.URLField(max_length=250, unique=True, verbose_name="URL"),
                ),
                (
                    "link_type",
                    models.CharField(
                        choices=[
                            ("artist", "Artist"),
                            ("album", "Album"),
                            ("track", "Track"),
                        ],
                        max_length=250,
                        verbose_name="Type",
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links",
                        to="spotify.Album",
                        verbose_name="Album",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links",
                        to="spotify.Artist",
                        verbose_name="Artist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Spotify Link",
                "verbose_name_plural": "Spotify Links",
            },
        ),
    ]
