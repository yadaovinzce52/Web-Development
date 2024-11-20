import os
from dotenv import load_dotenv, dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

load_dotenv()
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                               scope=scope))

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

year = input("Which year do you want to travel to? Type the date in this form YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{str(year)}", headers=header)

soup = BeautifulSoup(response.text, "html.parser")

songs = soup.find_all("h3", attrs={"class": "a-no-trucate"})
song_titles = [song.getText().strip() for song in songs]

