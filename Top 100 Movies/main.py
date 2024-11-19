import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)
top_movies = response.text

soup = BeautifulSoup(top_movies, "html.parser")
titles = soup.find_all("h3")

with open("movies.txt", "w", encoding="utf-8") as file:
    for title in titles[::-1]:
        file.writelines(f"{title.text}\n")

