import os
from logging import raiseExceptions
from pprint import pprint

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                               scope="playlist-modify-private",
                                               cache_path="token.txt"))

user = sp.current_user()
user_id = user["id"]

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

date = input("Which year do you want to travel to? Type the date in this form YYYY-MM-DD: ")
year = int(date.split('-')[0])
month = int(date.split('-')[1])
day = int(date.split('-')[2])


response = requests.get(f"https://www.billboard.com/charts/hot-100/{str(date)}", headers=header)

soup = BeautifulSoup(response.text, "html.parser")

songs = soup.find_all("h3", attrs={"class": "a-no-trucate"})
song_titles = [song.getText().strip() for song in songs]


songs_to_add = []

for song in song_titles:
    try:
        result = sp.search(q=f"track:{song}, year:{year}", type="track", limit=1)
        if len(result["tracks"]["items"]) == 0:
            raise ValueError
        song = result["tracks"]["items"][0]["uri"]
        songs_to_add.append(song)
    except ValueError:
        print(f"{song} does not exist in Spotify. Skipping.")

playlist = sp.user_playlist_create(user=user_id,
                                   name=f"Top 100 song week of {date}",
                                   public=False,
                                   collaborative=False,
                                   description=f"This playlist contains the top 100 songs on the week of {date}")

result = sp.playlist_add_items(playlist_id=playlist["id"], items=songs_to_add)