from fastapi import FastAPI, APIRouter, HTTPException,Response, status, Depends
from random import random, randrange
from fastapi.middleware.cors import CORSMiddleware

from pydantic_settings import BaseSettings, SettingsConfigDict
from app.database import Base, engine
from app.router import posts, users, auth, vote


from app.config import settings


# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get('/')
def root():
    return {"message": "Hello, World!"}

