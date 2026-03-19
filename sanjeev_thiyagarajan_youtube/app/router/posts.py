from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from typing import Optional, List

from oauth2 import get_current_user
import models
from database import Base, get_db, engine
from sqlalchemy.orm import Session
from typing import List
from schemas import PostCreate, PostUpdate, PostResponse, UserCreate, UserResponse
from utils import pwd_context, hash_password, verify_password


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]  
)




@router.post('/',status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # post_dict = post.dict()
    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post_dict["title"], 
    #                 post_dict["content"], 
    #                 post_dict["published"]))

    # new_post = cursor.fetchone()
    # conn.commit()

    """ with sql query using only orm """
    try:
        post_dict = post.dict()
        post_dict["owner_id"] = current_user.id
        # new_post = models.Post(title=post.title, content=post.content, published=post.published)
        new_post = models.Post(**post_dict)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post
    except Exception as err:
        pass


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def get_posts(
    db:Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user), 
    limit: int= 10, 
    skip: int= 0,
    order_by: str = "id",
    search: Optional[str] = None,
    group_by: Optional[str] = None
    ):
    try:
        db_query = db.query(models.Post)
        if search:
            db_query = db_query.filter(models.Post.title.contains(search) | models.Post.content.contains(search))
        posts = db_query.limit(limit).offset(skip).all()
        return posts
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(err)
        )


@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(
    post_id: int, 
    db:Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user),
    limit: int = 10
    ):

    """ using sql query """
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (post_id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # return post

    """ with sql query using only orm """
    post = db.query(models.Post).filter(models.Post.id == post_id).limit(1).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.put('/{post_id}', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def update_post(post_id: int, updated_post: PostUpdate, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    """ using sql query """
    # cursor.execute(""" select * from posts where id = %s""", (post_id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (updated_post.title, updated_post.content, updated_post.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # return {"post": updated_post}

    """ with sql query using only orm """
    update_datas = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not update_datas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    update_datas.title = updated_post.title
    update_datas.content = updated_post.content
    update_datas.published = updated_post.published
    db.commit()
    db.refresh(update_datas)
    return update_datas


@router.patch('/{post_id}', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def patch_post(post_id: int, updated_fields: dict, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    # for i, post in enumerate(post_data):
    #     if post["id"] == post_id:
    #         post_data[i] = {**post, **updated_fields}
    #         return post_data[i]
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    """ with sql query using only orm """
    db.query(models.Post).filter(models.Post.id == post_id).update(updated_fields )
    db.commit()
    return {"posts": "updated successfully"}

@router.delete('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def delete_post(post_id: int, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    """ using sql query """
    # cursor.execute(""" select * from posts where id = %s""", (post_id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (post_id,))
    # deleted_data = cursor.fetchone()
    # conn.commit()
    # return {"post": deleted_data}

    """ with sql query using only orm """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

