import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

DATE = "2020-09-10"
FILENAME = f"100songs-{DATE}"
URL_BILLBOARD = "https://www.billboard.com/charts/hot-100/"

## spotify identifiers

CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR CLIENT SECRET"

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
scope = "playlist-modify-private"
SPOTIPY_REDIRECT_URI = "http://example.com"
USERNAME = "YOUR USERNAME"
code = "YOUR CODE"

### STEP 1
# ________SCRAPE billboard 100 for song names _________

response = requests.get(f"{URL_BILLBOARD}{DATE}/")
print(f"{URL_BILLBOARD}{DATE}/")

content = BeautifulSoup(response.text, "html.parser")
list_titles = content.select(selector="ul li.o-chart-results-list__item h3")
song_list = [f"{item.getText().strip()}\n" for item in list_titles]

with open(FILENAME, "w") as file:
    file.writelines(song_list)

### STEP 2
# _________ Connect to spotify ____________

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               scope=scope, redirect_uri=SPOTIPY_REDIRECT_URI,
                                               cache_path="token.txt", username=USERNAME))
results = sp.current_user()
user_id = results["id"]
print(user_id)

### STEP 3
# ________ Create playlist and get ID _______

spotify_list_name = f"{DATE} Billboard 100"
# print(spotify_list_name)
playlist_ID = sp.user_playlist_create(user_id, name=spotify_list_name, public=False,
                                      description="playlist created by python from file")
print(playlist_ID)
print(playlist_ID["id"])
playlist_id = playlist_ID["id"]

###  STEP 4
# ________ Populate playlist ________________

year = DATE[:4]
tracks_list = []
with open(FILENAME, "r") as file:
    song_names = file.readlines()
for name in song_names:
    song = sp.search(q=f"track: {name} year: {year}", limit=1, offset=0, type='track', market=None)
    try:
        track_URI = song['tracks']['items'][0]['uri']
    except IndexError:
        pass
    else:
        tracks_list.append(track_URI)
        pprint.pprint(song['tracks']['items'][0]['uri'])
sp.user_playlist_add_tracks(user_id, playlist_id, tracks_list)

print(tracks_list)
