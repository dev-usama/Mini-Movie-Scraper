from fastapi import FastAPI, Depends
from pydantic import BaseModel
from jose import jwt
from app.config import settings, SessionLocal
from app.auth import verify_token
from app.models import Movie

app = FastAPI()
db = SessionLocal()

# Returns JWT token (no auth)
@app.post('/auth/login')
def login():
    token = jwt.encode({'name': 'usama'}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

# List all with pagination
@app.get('/movies')
def movies(page: int, limit: int, user=Depends(verify_token)):
    return "GET ALL MOVIES"

# Single movie details
@app.get('/movies/{id}')
def movies_by_id(user=Depends(verify_token)):
    return ""
@app.patch('movies/{id}')
def update_movie(user=Depends(verify_token)):
    return "Update title or genre (🔒 auth required)"

@app.delete('movies/{id}')
def delete_movie(user=Depends(verify_token)):
    return "Update title or genre (🔒 auth required)"
