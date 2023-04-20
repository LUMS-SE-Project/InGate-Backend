from datetime import datetime, timedelta
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import User, UserInDB, UserInSignUp
from app.schemas.token import Token, TokenData
from app.config.db import client
import app.config.secrets as SECRET

from app.auth.provider import oauth2_scheme, get_password_hash, verify_password, create_access_token, return_user
from app.utils.signUp import verify_email as SignUpVerifyEmail
from app.utils.Login import verify_email as LoginVerifyEmail
from app.utils.Login import get_password, get_info

router = APIRouter()

@router.get("/")
def index():
    return {"message": "Hello World!"}

@router.post('/signup')
async def signup(data : UserInSignUp):
    try :
        await SignUpVerifyEmail(data.email)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
    
    hashed_password = get_password_hash(data.password)

    # create an object for the db insertion
    db_obj = UserInDB(
        username=data.username, 
        email=data.email, 
        name=data.name, 
        hashed_password=hashed_password, 
        isAdmin=False,
        gender= data.gender,
        number = data.number,
        alumnus=False,
        status=False,
        )
    
    table = client["SEProject"]["User"]

    table.insert_one(dict(db_obj))
    return {"signup": "Signup successful"}

@router.post('/login', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=SECRET.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "isAdmin": user.isAdmin
        }

@router.get("/current-user")
async def current_user(token : str = Depends(oauth2_scheme)):
    try:
        user = await return_user(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data_to_return = dict(
        username=user.username,
        email=user.email,
        name=user.name,
        isAdmin = user.isAdmin
    )

    return {
        "data" : data_to_return
    }

@router.post('/forgot-password')
async def forgot_password(data : dict):
    email = data["email"]
    password = data["password"]
    user_table = client["SEProject"]["User"]
    hashed_password = get_password_hash(password)
    user_table.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})
    return {"message": "Password Updated"}


async def authenticate_user(username: str, password: str):
    try:
        user = await get_info(username)
    except:
        raise Exception("Invalid email")

    # get the user password from db
    try:
        hashed_password = await get_password(username)
    except:
        raise Exception("Invalid password/email")

    # verify the password
    password_verify = verify_password(password, hashed_password)

    if password_verify:
        return user
    else:
        raise Exception("Invalid password")