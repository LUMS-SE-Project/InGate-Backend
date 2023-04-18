from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.user import User, UserInDB
from app.schemas.token import TokenData

from app.config.secrets import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.config.db import client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def return_user(token: Annotated[str, Depends(oauth2_scheme)]):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        content = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = content.get("sub")
        if username is None:
            raise exception
        
        token_data = TokenData(username=username)

    except JWTError:
        raise exception 
    
    # get user from db
    table = client["SEProject"]["User"]
    user = table.find_one({"email": token_data.username})

    if not user:
        raise exception
    
    print("returning", user)
    return UserInDB(**user)

def get_current_user(user: Annotated[UserInDB, Depends(return_user)]):
    if user.status == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user