from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from typing import Optional, List
from random import random, randrange
from psycopg2.extras import RealDictCursor
import psycopg2
import time
import models
from database import Base, get_db, engine
from sqlalchemy.orm import Session
from typing import List
from schemas import UserCreate, UserResponse
from utils import pwd_context, hash_password, verify_password


router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

# app = FastAPI()




# user related data
@router.post('/',status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db:Session = Depends(get_db)):

    """ with sql query using only orm """
    user_dict = user.dict()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    hashed_password = hash_password(user_dict["password"])
    user_dict["password"] = hashed_password
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


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



# @app.put('/users/{user_id}', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
# def update_user(user_id: int, updated_user: UserCreate, db:Session = Depends(get_db)):

#     """ with sql query using only orm """
#     update_datas = db.query(models.User).filter(models.User.id == user_id).first()
#     if not update_datas:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


#     hash_password  = updated_user.password
#     update_datas.email = updated_user.email
#     update_datas.password = updated_user.password
#     db.commit()
#     db.refresh(update_datas)
#     return update_datas



@router.delete('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def delete_user(user_id: int, db:Session = Depends(get_db)):
    """ with sql query using only orm """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}