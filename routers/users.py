from user_models import User as UserModel
from fastapi import APIRouter, Depends, HTTPException
from schemas import UserCreate
from database import get_db
from sqlalchemy.orm import Session
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = UserModel(
        username = user.username,
        password = hashed_password
    )

    db.add(new_user)

    db.commit()

    return new_user

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