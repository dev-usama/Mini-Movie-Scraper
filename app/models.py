from typing import Optional
from sqlmodel import Field, SQLModel

class Movie(SQLModel, table=True):
    __tablename__ = "movie"
    
    imdb_id: str = Field(primary_key=True)
    title: str = Field(nullable=False)
    thumbnail_url: Optional[str] = Field(default=None, nullable=True)
    genres: Optional[str] = Field(default=None, nullable=True)
    release_year: Optional[int] = Field(default=None, nullable=True)
    source_url: str = Field(unique=True, nullable=False)