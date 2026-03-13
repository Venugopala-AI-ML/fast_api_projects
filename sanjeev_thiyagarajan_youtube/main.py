from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import random, randrange


app = FastAPI()


post_data  = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post."
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post."
    },
]


class PostData(BaseModel):
    id: int
    title: str
    content: str
    create_at: str
    published_at : bool = True
    rating : Optional[int]


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    create_at: str
    published_at: bool = True
    rating: Optional[int]

@app.get('/')
def root():
    return {"message": "Hello, World!"}


@app.post('/posts', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostData) -> PostResponse:
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 10000000)
    post_data.append(post_dict)
    return PostResponse(**post_dict)


@app.get('/posts', response_model=List[PostResponse], status_code=status.HTTP_200_OK)
def get_posts():
    return post_data

@app.get('/posts/{post_id}', response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int):
    for post in post_data:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.put('/posts/{post_id}')
def update_post(post_id: int, updated_post: PostData):
    for i, post in enumerate(post_data):
        if post["id"] == post_id:
            post_data[i] = {**post, **updated_post.dict()}
            return post_data[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.patch('/posts/{post_id}')
def patch_post(post_id: int, updated_fields: dict):
    for i, post in enumerate(post_data):
        if post["id"] == post_id:
            post_data[i] = {**post, **updated_fields}
            return post_data[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.delete('/posts/{post_id}', status_code=status.HTTP_200_OK)
def delete_post(post_id: int):
    for id, post in enumerate(post_data):
        if post['id'] == post_id:
            del post_data[id]
            # post_data.pop(id)
            return Response(status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


