# Movie Scrapper Web Service

## Installation

### Dependencies
    uv sync

### Populate the data
    sudo -u postgres psql -d postgres -f schema.sql
    cd app
    uv run scrape.py

### To run the project
    uv run fastapi dev

