CREATE TABLE movie (
    imdb_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    thumbnail_url VARCHAR,
    genres VARCHAR,
    release_year INTEGER,
    source_url VARCHAR
);