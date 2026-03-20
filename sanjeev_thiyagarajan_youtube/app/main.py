from fastapi import FastAPI, APIRouter, HTTPException,middleware,Response, status, Depends
from random import random, randrange

from pydantic_settings import BaseSettings, SettingsConfigDict
import models
from database import Base, engine
from router import posts, users, auth, vote
import os

from config import settings


# Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
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

