import asyncio
import httpx
from config import SessionLocal, settings
from models import Movie

OMDB_URL = "http://www.omdbapi.com/"
OMDB_API_KEY = settings.postgres_url

MOVIE_TITLES = [
    "The Matrix", "Inception", "Interstellar", "The Dark Knight", "Gladiator",
    "Avatar", "Titanic", "The Avengers", "Iron Man", "Pulp Fiction",
    "Fight Club", "Forrest Gump", "Spiderman", "Batman", "Superman",
    "Star Wars", "Jurassic Park", "Jaws", "Alien", "Predator",
    "The Terminator", "Die Hard", "Goodfellas", "The Godfather", "Scarface",
    "Casino", "Heat", "Se7en", "The Prestige", "Memento",
    "The Departed", "Whiplash", "La La Land", "Toy Story", "Up",
    "WALL-E", "Ratatouille", "The Lion King", "Aladdin", "Frozen",
    "Shrek", "Mad Max: Fury Road", "Dune", "Blade Runner 2049", "The Revenant",
    "Joker", "Parasite", "Get Out", "The Sixth Sense", "Unbreakable"
]

async def fetch_and_populate():
    db = SessionLocal()
    saved_count = 0

    print(f"Connecting to Postgres to process up to {len(MOVIE_TITLES)} records...\n")

    async with httpx.AsyncClient(timeout=10.0) as client:
        for title in MOVIE_TITLES:
            try:
                params = {
                    "apikey": OMDB_API_KEY,
                    "t": title,
                    "type": "movie"
                }
                response = await client.get(OMDB_URL, params=params)
                
                if response.status_code != 200:
                    continue
                    
                data = response.json()
                if data.get("Response") == "False" or not data.get("imdbID"):
                    print(f" -> Skipped: '{title}' not found on OMDb.")
                    continue

                imdb_id = data.get("imdbID")

                existing = db.query(Movie).filter(Movie.imdb_id == imdb_id).first()
                if existing:
                    print(f" -> Skipped: '{data.get('Title')}' already exists in database.")
                    continue

                release_year = data.get("Year")
                parsed_year = int(release_year[:4]) if release_year and release_year[:4].isdigit() else None

                new_movie = Movie(
                    imdb_id=imdb_id,
                    title=data.get("Title"),
                    thumbnail_url=data.get("Poster") if data.get("Poster") != "N/A" else None,
                    genres=data.get("Genre") if data.get("Genre") != "N/A" else None,
                    release_year=parsed_year,
                    source_url=f"https://www.imdb.com/title/{imdb_id}/"
                )
                
                db.add(new_movie)
                db.commit()
                
                saved_count += 1
                print(f" -> Saved: '{new_movie.title}' ({imdb_id}) [{saved_count}/50]")
                
                await asyncio.sleep(0.2)

            except Exception as e:
                print(f" -> Error processing target '{title}': {e}")
                db.rollback()

    db.close()
    print(f"\nFinished execution! Successfully committed {saved_count} movies into Postgres.")

if __name__ == "__main__":
    asyncio.run(fetch_and_populate())