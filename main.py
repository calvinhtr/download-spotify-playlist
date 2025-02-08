import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from pytubefix import YouTube, Search
from pytubefix.cli import on_progress
from mutagen.mp4 import MP4
from typing import List

## TESTING CODE FOR DOWNLOADING AUDIO

# yt = YouTube('https://www.youtube.com/watch?v=zRZHpWxCcYs&ab_channel=Jaeguchi', use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
# print(yt.title)
# # get audio only
# video = yt.streams.get_audio_only()
# # download file
# out_file = video.download(output_path=os.getcwd())
# # rename file to mp3
# base, ext = os.path.splitext(out_file)
# new_file = base + '.mp3'
# os.rename(out_file, new_file)

## TESTING CODE FOR SEARCHING AUDIO

# s = Search('crazy le sserafim lyrics')
# for video in s.videos:
#     print(f'Title: {video.title}')
#     print(f'URL: {video.watch_url}')
#     print(f'Duration: {video.length} sec')
#     print('---')

## TESTING CODE FOR SEARCHING AND DOWNLOADING

# search = 'David Guetta Le Sserafim Crazy'
# s = Search(search + 'lyrics')

# yt = YouTube(s.videos[0].watch_url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
# print(f'downloading: {s.videos[0].title}')
# video = yt.streams.get_audio_only()
# out_file = video.download(output_path=os.getcwd())
# # rename file to mp3
# # base, ext = os.path.splitext(out_file)
# new_file = search + '.mp3'
# os.rename(out_file, new_file)

# TEST SPOTIFY CODE

# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

## WORKING CODE

def updateArtist(path: str, artist_names: List[str]):
    audio = MP4(path)
    audio['©ART'] = []

    for artist in artist_names:
        audio['©ART'].append(artist)
    audio.save(path)


def downloadSong(song_title: str, artist_names: List[str], output_path: str):
    print(f"Downloading {song_title}")
    # Perform search and get first video in search. Prayge it's the right one
    search_title = song_title
    for artist in artist_names:
        search_title += " " 
        search_title += artist
    s = Search(search_title + ' lyrics')
    # Find a version with no slashes
    ind = 0
    while True:
        if "/" not in s.videos[ind].title:
            break
        ind += 1
    yt = YouTube(
        s.videos[ind].watch_url, 
        use_oauth=True, 
        allow_oauth_cache=True, 
        # on_progress_callback=on_progress
        )
    # Retrieve audio
    video = yt.streams.get_audio_only()
    # Download audio
    out_file = video.download(output_path=output_path)
    new_file = output_path + '/' + song_title + '.m4a'
    os.rename(out_file, new_file)

    # Update artist name
    updateArtist(new_file, artist_names)

# Load .env
load_dotenv()

# Init Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

# Get list of all playlists
results = sp.current_user_playlists()
# Add all items in the current page
playlists = results['items']

# Add subsequent pages if there are any
while results['next']:
    results = sp.next(results)
    playlists.extend(results['items'])
    
# Iterate through playlists
for playlist in playlists:
    playlist_name = playlist['name']
    output_path = os.getcwd() + f'/{playlist_name}'
    print(f'Updating {playlist_name}')
    songs = sp.playlist_items(playlist['id'])['items']
    for song in songs:
        song_name = song['track']['name']
        artists_unprocessed = song['track']['artists']
        artists_processed = []
        for artist in artists_unprocessed:
            artists_processed.append(artist['name'])
        
        # Skip if file already downloaded
        if os.path.isfile(output_path + '/' + song_name + '.m4a'):
            print(f"Skipping {song_name}")
            continue

        # Retry mechanism
        tries = 3
        for i in range(tries):
            try:
                downloadSong(song_name, artists_processed, output_path)
            except:
                if i < tries - 1:
                    "Reattempting..."
                    continue
                else:
                    raise
            break

        
