from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True 

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass



class UserBase(BaseModel):
    email: EmailStr


class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
    

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True






class UserCreate(UserBase):
    password: str





class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(UserBase):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class PasswordChangeRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] | None = None

