




from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from requests import models
from sqlalchemy.orm import Session
from starlette import status
import schemas, database, models




SECRET_KEY = "bJfX49Scdo6xVfIyXLQ2FXLmMiktaLywzuENMnssMd8"  # Replace with a strong secret key
ALGORITHM = "HS256"  # Replace with a strong algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Replace with a strong token expiration time

# This tells FastAPI where to look for
#  the token (the /login URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Helper functions that takes user data
def create_access_token(data: dict):
    """
    Create an access token for the given data.
    explain little more about this 

    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(user_id= id)

    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: database.Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if not user:
        raise credentials_exception
    return user