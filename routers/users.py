from user_models import User as UserModel
from fastapi import APIRouter, Depends
from schemas import UserCreate
from database import get_db
from sqlalchemy.orm import Session
from security import hash_password

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