from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from typing import Optional, List
from random import random, randrange
import time
from app import models
from database import Base, get_db, engine
from sqlalchemy.orm import Session
from typing import List
from schemas import UserResponse, Vote
from utils import pwd_context, hash_password, verify_password
from oauth2 import get_current_user



router = APIRouter(
    prefix='/votes',
    tags=["Votes"]
)

# app = FastAPI()




# user related data
@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote, 
    db:Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
    ):

    """ with sql query using only orm """
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found with the id: {vote.post_id} does not exist")

    

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()


    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already voted for this post")
        
        # Create a new vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'messages': 'Vote added successfully'}
    else:
        # Delete an existing vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        
        vote_query.delete(synchronize_session=False)   
        db.commit()
        return {'messages': 'Vote deleted successfully'}


@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get('/', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users