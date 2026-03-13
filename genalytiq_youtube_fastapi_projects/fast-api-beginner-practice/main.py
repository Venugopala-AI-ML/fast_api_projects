from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app  = FastAPI()



class Student(BaseModel):
    name: str
    age: int
    roll: int


@app.get("/")
def get_post(name: str, age: Optional[int] = None):
    return {"message": {"name": name, "age": age, "roll": "roll"}}

@app.post('/posts') 
def create_post(student: Student):
    return {"message": {"name": student.name, "age": student.age, "roll": student.roll}}

@app.put('/posts/{post_id}')
def update_post(post_id: int):
    return {"message": f"Post updated with ID: {post_id}"}              






