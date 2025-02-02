import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from pytubefix import YouTube, Search
from pytubefix.cli import on_progress

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
    # print(playlist['id'])
    # print(sp.playlist_items(playlist['id']))
    print(f'Updating {playlist_name}')
    songs = sp.playlist_items(playlist['id'])['items']
    for song in songs:
        name = song['track']['name']
        artists = song['track']['artists']
        searchTitle = name + " -"
        for artist in artists:
            searchTitle += " "
            searchTitle += artist['name']
        
        # Skip if file already downloaded
        if os.path.isfile(output_path + '/' + searchTitle + '.mp3'):
            print(f"Skipping {searchTitle}")
            continue
        # TODO: RETRY MECHANISM
        tries = 3
        for i in range(tries):
            # functionify this
            try:
                print(f"Downloading {searchTitle}")
                # Perform search and get first video in search. Prayge it's the right one
                s = Search(searchTitle + ' lyrics')
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
                # Download video
                out_file = video.download(output_path=output_path)
                new_file = output_path + '/' + searchTitle + '.mp3'
                os.rename(out_file, new_file)
            except:
                if i < tries - 1:
                    "Reattempting..."
                    continue
                else:
                    raise
            break

        
