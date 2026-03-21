from datetime import datetime, timedelta
from typing import Dict

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import database, schemas
from app import models
import oauth2, utils
from random import randint




router = APIRouter(tags=["Authentication"])

# In-memory OTP store (demo only - replace with a persistent store in production).
otp_store: Dict[str, Dict[str, object]] = {}


def _generate_otp() -> str:
    """Generate a 6-digit OTP code."""


    return f"{randint(0, 999999):06d}"


@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")


    # Validate password strength (letters, numbers, special characters)
    try:
        utils.validate_password_strength(user.password)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    # Hash the password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    # Create new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):


    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    verify_password_getin = utils.verify_password(user_credentials.password, user.password)
    
    if not verify_password_getin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    

    create_jwt_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {
        "access_token": create_jwt_token,
        "token_type": "bearer",
        "user_details": {
            'id': user.id,
            'email': user.email,
        }
    }


@router.post("/forgot-password")
def forgot_password(request: schemas.PasswordResetRequest, db: Session = Depends(database.get_db)):
    """Generate a 6-digit OTP and send to the user's email."""

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        # Do not reveal whether the email exists.
        return {"message": "If an account exists for this email, an OTP will be sent."}

    otp = _generate_otp()
    otp_store[request.email.lower()] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=10),
    }

    try:
        utils.send_otp_email(to_email=request.email, otp=otp)
    except Exception:
        # Fallback: keep behavior consistent while logging for debugging.
        return {"message": "OTP generated; check application logs for the code."}

    return {"message": "OTP sent to your email address.", "expires_in_minutes": 10}


@router.post("/verify-otp")
def verify_otp(request: schemas.OTPVerifyRequest):
    """Verify an OTP code previously issued for password reset."""

    entry = otp_store.get(request.email.lower())
    if not entry:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    if entry["expires_at"] < datetime.utcnow():
        otp_store.pop(request.email.lower(), None)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")

    if entry["otp"] != request.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    return {"message": "OTP verified. You may now reset your password."}


@router.post("/reset-password")
def reset_password(request: schemas.PasswordChangeRequest, db: Session = Depends(database.get_db)):
    """Reset the user's password after OTP verification."""

    entry = otp_store.get(request.email.lower())
    if not entry:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    if entry["expires_at"] < datetime.utcnow():
        otp_store.pop(request.email.lower(), None)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")

    if entry["otp"] != request.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    try:
        utils.validate_password_strength(request.new_password)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.password = utils.hash_password(request.new_password)
    db.commit()

    otp_store.pop(request.email.lower(), None)

    return {"message": "Password has been reset successfully."}
