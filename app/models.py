from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movie"
    imdb_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    genres = Column(String, nullable=True)
    release_year = Column(Integer, nullable=True)
    source_url = Column(String, unique=True, nullable=False)