# Movie Scrapper Web Service

## Installation

### Dependencies
    uv sync

### Apply migrations
    sudo -u postgres createdb -U postgres movie_db
    uv run alembic upgrade head

### To run the project
    uv run fastapi dev

