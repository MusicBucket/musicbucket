from typing import Dict, List, Optional

import requests
import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    BASE_API_URL = "https://api.spotify.com/v1"

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        )
        self.client = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )

    def search_links(self, query: str, entity_type: str) -> List:
        from spotify.models import SpotifyLink

        """
        Searches for a list of coincidences in Spotify
        :param query: query string term
        :param entity_type: EntityType
        :return: list of results
        """
        search_result = self.client.search(query, type=entity_type)
        if entity_type == SpotifyLink.TYPE_ARTIST:
            search_result = search_result["artists"]["items"]
        elif entity_type == SpotifyLink.TYPE_ALBUM:
            search_result = search_result["albums"]["items"]
        elif entity_type == SpotifyLink.TYPE_TRACK:
            search_result = search_result["tracks"]["items"]
        return search_result

    def get_link_data(self, url: str) -> Dict:
        """
        Resolves the name and the genre of the artist/album/track from a link
        Artist: 'spotify:artist:id'
        Album: 'spotify:album:id'
        Track: 'spotify:track:id'
        """
        from spotify.models import SpotifyLink

        # Gets the entity id from the Spotify link:
        # https://open.spotify.com/album/*1yXlpa0dqoQCfucRNUpb8N*?si=GKPFOXTgRq2SLEE-ruNfZQ
        entity_id = SpotifyLink.get_entity_id_from_url(url)
        link_type = SpotifyLink.get_entity_id_from_url(url)
        data = {}
        if link_type == SpotifyLink.TYPE_ARTIST:
            uri = f"spotify:artist:{entity_id}"
            artist = self.client.artist(uri)
            data["artist"] = artist["name"]
            data["genres"] = artist["genres"]
        elif link_type == SpotifyLink.TYPE_ALBUM:
            uri = f"spotify:album:{entity_id}"
            album = self.client.album(uri)
            data["album"] = album["name"]
            data["artist"] = album["artists"][0]["name"]
            if album["genres"]:
                data["genres"] = album["genres"]
            else:
                album_artist = self.client.artist(album["artists"][0]["id"])
                data["genres"] = album_artist["genres"]
        elif link_type == SpotifyLink.TYPE_TRACK:
            uri = f"spotify:track:{entity_id}"
            track = self.client.track(uri)
            data["track"] = track["name"]
            data["album"] = track["album"]["name"]
            data["artist"] = track["artists"][0]["name"]
            track_artist = self.client.artist(track["artists"][0]["id"])
            data["genres"] = track_artist["genres"]
        return data

    def get_all_artist_albums(self, artist) -> List:
        albums_response = self.client.artist_albums(
            artist.spotify_id, album_type="album,single,compilation", limit=50
        )
        albums_simpl = albums_response["items"]
        while albums_response["next"]:
            albums_response = self.client.next(albums_response)
            albums_simpl.extend(albums_response["items"])
        albums_full = []
        for album_simpl in albums_simpl:
            albums_full.append(self.client.album(album_simpl["id"]))
        return albums_full

    def get_artist_top_track(self, artist) -> Dict:
        top_track = self.client.artist_top_tracks(artist.spotify_id)["tracks"][0]
        return top_track

    def get_album_first_track(self, album) -> Dict:
        first_track = self.client.album_tracks(album.spotify_id)["items"][0]
        return first_track

    @staticmethod
    def refresh_token(refresh_token: str) -> Dict:
        # TODO: Extract to a userclient.py with user based spotify methods
        url = f"https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = requests.post(url, data, headers)
        return response.json()

    def get_users_recently_played_tracks(
        self,
        user,
        after_ms: Optional[int] = None,
        before_ms: Optional[int] = None,
        limit: int = 50,
    ) -> Dict:
        # TODO: Extract to a userclient.py with user based spotify methods
        url = f"{self.BASE_API_URL}/me/player/recently-played"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user.tokens.access_token}",
        }
        params = {"limit": limit}
        if before_ms:
            params["before"] = before_ms
        if after_ms:
            params["after"] = after_ms
        response = requests.get(url, params=params, headers=headers)
        return response.json()
