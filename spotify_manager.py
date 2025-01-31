import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_USER_NAME,
)


class SpotifyManager:
    """
    This class manages interaction with the Spotify API.
    It allows for searching songs and creating playlists in a Spotify user account.
    """

    def __init__(self):
        """
        Initializes the SpotifyManager instance by authenticating with the Spotify API.
        """
        # OAuth authentication manager setup with necessary parameters.
        self.auth_manager = SpotifyOAuth(
            scope="playlist-modify-private",  # Defines the required permissions.
            redirect_uri=SPOTIFY_REDIRECT_URI,  # Registered redirect URI for the Spotify application.
            client_id=SPOTIFY_CLIENT_ID,  # Client ID for the Spotify application.
            client_secret=SPOTIFY_CLIENT_SECRET,  # Client secret for the Spotify application.
            show_dialog=True,  # Show authentication dialog every time.
            cache_path="token.txt",  # File where the access token is stored.
            username=SPOTIFY_USER_NAME,  # Spotify username.
        )
        # Create the Spotify client using the authentication manager.
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def search_song(self, song_name, artist_name):
        """
        Searches for a song on Spotify by name and artist and returns its Spotify URI.

        Parameters:
            song_name (str): Name of the song to search for.
            artist_name (str): Name of the artist of the song to search for.

        Returns:
            str: Spotify URI of the found song, or None if not found.
        """
        query = f"track:{song_name} artist:{artist_name}"
        result = self.sp.search(q=query, type="track", limit=1)
        tracks = result["tracks"]["items"]
        if tracks:
            return tracks[0]["uri"]
        return None

    def create_spotify_playlist(self, user_id, date, song_artist_list):
        """
        Creates a playlist in the Spotify user's account and adds the provided songs.

        Parameters:
            user_id (str): Spotify user ID.
            date (str): Date to be used in the playlist name.
            song_artist_list (list): List of songs and artists to add to the playlist.
        """
        # Define the name and description of the new playlist.
        playlist_name = f"Billboard Top 100 - {date}"
        playlist_description = "Playlist generated with Billboard's top 100 songs."

        # Creates the playlist on Spotify and gets its ID.
        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False,
            description=playlist_description,
        )
        playlist_id = playlist["id"]

        # Searches for the Spotify URIs of the songs and adds them to the playlist.
        uris = []
        for song_artist in song_artist_list:
            song_name, artist_name = song_artist.split(" by ")
            uri = self.search_song(song_name, artist_name)
            if uri:
                uris.append(uri)

        # Adds the songs to the playlist and notifies the user.
        if uris:
            self.sp.playlist_add_items(playlist_id=playlist_id, items=uris)
            print(f"{len(uris)} songs were added to the playlist '{playlist_name}'.")
        else:
            print("No songs could be added to the playlist.")
