from backend.app.database.models.user import User as UserModel
from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.database.database import get_db
from sqlalchemy.orm import Session
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) |
        (UserModel.email == user.email)
    ).first()

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code = 400,
                detail = "Username is already registered."
            )

        if existing_user.email == user.email:
            raise HTTPException(
                status_code = 400,
                detail = "Email is already registered."
            )

    hashed_password = hash_password(user.password)

    new_user = UserModel(
        username = user.username,
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)

    db.commit()

    return new_user

@router.get("/check-username")
def check_username(username: str, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        UserModel.username == username
    ).first()

    return {
        "available": existing_user is None
    }

@router.post("/login")
def login_user(user: OAuth2PasswordRequestForm = Depends(), 
               db: Session = Depends(get_db)):
    
    existing_user = db.query(UserModel).filter(
        UserModel.username == user.username).first()
    
    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password") 
    access_token = create_access_token(
        existing_user.id,
        existing_user.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }