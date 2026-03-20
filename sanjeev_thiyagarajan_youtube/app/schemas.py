from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True 

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass

class UserBase(BaseModel):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True
    

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)


class PostResponse(BaseModel):
    Post: Post
    votes: int


    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] | None = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore


class PasswordResetRequest(UserBase):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class PasswordChangeRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str



