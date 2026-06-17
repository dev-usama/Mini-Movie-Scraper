from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt
from sqlmodel import Session, select
from app.config import settings, get_session
from app.auth import verify_token
from app.models import Movie

app = FastAPI()
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
def movies(
    page: int, 
    limit: int, 
    user=Depends(verify_token), 
    db: Session = Depends(get_session)
):
    statement = (
        select(Movie)
        .order_by(Movie.imdb_id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    items = db.exec(statement).all()    
    return items


@app.get('/movies/{id}', status_code=status.HTTP_200_OK)
def movies_by_id(
    id: str, 
    user=Depends(verify_token), 
    db: Session = Depends(get_session)
):
    movie = db.get(Movie, id)
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with IMDb ID '{id}' not found."
        )
        
    return movie

@app.patch('/movies/{id}', status_code=status.HTTP_200_OK)
def update_movie(id: str, data: MovieUpdate, user=Depends(verify_token), db: Session = Depends(get_session)):
    movie = db.get(Movie, id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with IMDb ID '{id}' not found."
        )
    update_data = data.model_dump(exclude_unset=True)    
    for key, value in update_data.items():
        setattr(movie, key, value)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    
    return {"message": "Record updated successfully", "movie": movie}

@app.delete('/movies/{id}', status_code=status.HTTP_200_OK)
def delete_movie(
    id: str, 
    user=Depends(verify_token), 
    db: Session = Depends(get_session)  # Updated dependency
):
    # Fetch the movie using the primary key
    movie = db.get(Movie, id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with IMDb ID '{id}' not found."
        )
        
    db.delete(movie)
    db.commit()  # Remember to commit the transaction to save the deletion
    
    return {"message": "Record deleted successfully"}