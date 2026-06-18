# Movie Scrapper Web Service

## Installation

### Dependencies
    uv sync

### Apply migrations
    sudo -u postgres createdb -U postgres movie_db
    uv run alembic upgrade head
    cd app
    uv run scrape.py (For web scraping to store movie data in database)
    uv run movie_api (For calling OMDB API to store movie data in database)


### To run the project
    Go to the project root directory
    uv run fastapi dev

