from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime
import jwt

# Password hashing context 
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    """Hash a password using the defined password context."""

    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    """Verify a password against its hash."""
    return pwd_context.verify(password, hashed_password)
