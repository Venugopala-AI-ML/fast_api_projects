from pydantic import BaseModel, EmailStr


# schemas for new users
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role:str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True