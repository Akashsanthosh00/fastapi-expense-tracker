from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
import datetime
import os
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id, username):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        ) # here the pyJWT takes the token apart -> HEADER.PAYLOAD.SIGNATURE
        #THEN IT WILL CREATE A NEW SIGNATURE USING THE HEADER AND PAYLOAD DATA FROM THE TOKEN, AND
        # SECRET_KEY THAT WE PASSED, NOW IT WILL COMPARE THE SIGNATURE IN THE TOKEN AND
        # THE NEW SIGNATURE THAT WE CREATED, IF THEY DON'T MATCH NO AUTHORIZATION
        # THE IDEA BEHIND IS WE CANNOT CHANGE THE SIGNATURE PART, ONLY THE USER CAN BYPASS USING THE MODIFYING
        # DATAS INSIDE THE PAYLOAD, IF MODIFIED IT WILL DEFINITELY CREATES A NEW SIGNATURE WHICH WILL BE UNMATCH
        #FOR THE SIGNATURE IN THE CURRENT TOKEN
        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )