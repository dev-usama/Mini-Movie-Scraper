from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt
from app.config import settings, SessionLocal
from app.auth import verify_token
from app.models import Movie

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    genres: Optional[str] = None
    release_year: Optional[int] = None
    source_url: Optional[str] = None

# Returns JWT token (no auth)
@app.post('/auth/login')
def login():
    token = jwt.encode({'name': 'usama'}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

# List all with pagination
@app.get('/movies', status_code=status.HTTP_200_OK)
def movies(page: int, limit: int, user=Depends(verify_token), db=Depends(get_db)):
    items = (
        db.query(Movie)
        .order_by(Movie.imdb_id)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return items

# Single movie details
@app.get('/movies/{id}', status_code=status.HTTP_200_OK)
def movies_by_id(id: str, user=Depends(verify_token), db=Depends(get_db)):
    movie = db.query(Movie).filter(Movie.imdb_id == id).first()
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with IMDb ID '{imdb_id}' not found."
        )
        
    return {
        "imdb_id": movie.imdb_id,
        "title": movie.title,
        "thumbnail_url": movie.thumbnail_url,
        "genres": movie.genres,
        "release_year": movie.release_year,
        "source_url": movie.source_url
    }

@app.patch('/movies/{id}', status_code=status.HTTP_200_OK)
def update_movie(id:str, data:MovieUpdate, user=Depends(verify_token), db=Depends(get_db)):
    movie = db.query(Movie).filter(Movie.imdb_id == id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with IMDb ID '{imdb_id}' not found."
        )
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return f"Record updated successfully, {movie}"

@app.delete('/movies/{id}', status_code=status.HTTP_200_OK)
def delete_movie(id: str, user=Depends(verify_token), db=Depends(get_db)):
    movie = db.query(Movie).filter(Movie.imdb_id == id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with IMDb ID '{imdb_id}' not found."
        )
    db.delete(movie)
    return "Record deleted successfully"
