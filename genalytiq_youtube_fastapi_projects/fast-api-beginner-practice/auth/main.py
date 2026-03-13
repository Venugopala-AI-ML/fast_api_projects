from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError


# why we need this is screct key is 
SECRET_KEY  = "bJfX49Scdo6xVfIyXLQ2FXLmMiktaLywzuENMnssMd8" # Replace with a strong secret key
ALGORITHM = "HS256" # Replace with a strong algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Replace with a strong token expiration time

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


app = FastAPI()


@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()

        existing_username = db.query(models.User).filter(models.User.username == user.username).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        if existing_username:
            raise HTTPException(status_code=400, detail="User with this username already exists")

        # Hash the password
        hashed_password = utils.hash_password(user.password)

        # create New user
        new_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # # Create new user
        # new_user = models.User(
        # email=user.email, 
        # username=user.username, 
        # hashed_password=hashed_password, 
        # role=user.role
        # )
        # db.add(new_user)
        # db.commit()
        # db.refresh(new_user)

        # Create access token
        access_token = create_access_token(data={"sub": new_user.id})

        return {
            "access_token": access_token, 
            "token_type": "bearer", 
            "user_details": {
                'id': new_user.id, 
                'email': new_user.email, 
                'username': new_user.username,
                "role": new_user.role
                }
            }
    
    except Exception as err:
        db.rollback()
        return {"error": str(err), "status": status.HTTP_400_BAD_REQUEST}
    
@app.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Create access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_details": {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            "role": user.role
        }
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
        )
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get('role')
        if username is None or role is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
    return {"username": username, "role": role}


@app.get('/protected')
def protected_route(current_user: dict = Depends(get_current_user)):

    return {"message":"You are authenticated!", "user": current_user}


def required_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get('role')
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker



@app.get("/profile")
def profile(current_user: dict = Depends(required_roles(["user", "Software Developer"]))):
    return {"message": f"Profile of {current_user['username']} ({current_user['role']})"}



@app.get('/user')
def admin_route(current_user: dict = Depends(required_roles(["user"]))):
    return {"message": "Welcome, admin!"}

@app.get('/user/dashboard')
def user_dashboard(current_user: dict = Depends(required_roles(['user']))):
    return {"message": "Welcome to your dashboard!", "user": current_user.get('username')}

@app.get('/user/profile')
def user_profile(current_user: dict = Depends(required_roles(['user']))):
    return {"message": f"Profile of {current_user['username']} ({current_user['role']})"}