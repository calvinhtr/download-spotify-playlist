import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

results = sp.current_user_playlists()
# Add all items in the current page
playlists = results['items']

# Add subsequent pages if there are any
while results['next']:
    results = sp.next(results)
    playlists.extend(results['items'])

for playlist in playlists:
    print(playlist['name'])