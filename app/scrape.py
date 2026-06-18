import asyncio
from models import Movie
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs
from sqlmodel import Session
from config import db_engine, settings

response = requests.get("https://www.filmcrave.com/list_top_movie.php?yr=2026")

soup = BeautifulSoup(response.text, 'html.parser')

imgs = soup.find_all(name="img", class_="movie-fixed")

data = []
async def populate_data():
    try:
        with Session(db_engine) as db:
            for img in imgs:
                a_tag = img.parent
                href = a_tag["href"]
                movie_id = parse_qs(urlparse(href).query)["id"][0]
                new_movie = Movie(
                                    imdb_id=movie_id,
                                    title=img.get('title'),
                                    thumbnail_url=img.get('src'),
                                    source_url=f"https://www.filmcrave.com{href}"
                            )
                db.add(new_movie)
                db.commit()
                print(f" -> Saved: '{new_movie.title}' ")
                await asyncio.sleep(0.2)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    asyncio.run(populate_data())
