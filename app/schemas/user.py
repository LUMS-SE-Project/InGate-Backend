from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from app.schemas.restaurant import ItemInCart

# change for gender
class UserInSignUp(BaseModel):
    username : str
    email : str
    name : str
    password : str
    alumnus : bool
    gender : str


class User(BaseModel):
    username : str | None = None
    email : str
    name : str | None = None
    password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None
    isAdmin : bool | None = None

class UserInDB(BaseModel):
    username : str | None = None
    email : str
    name : str | None = None
    hashed_password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None
    gender: str | None = None
    isAdmin : bool | None = None

class Login(BaseModel):
    username: str
    password: str

class Order(BaseModel):
    items: list[ItemInCart]
    gender_preference: str
    partial_order: bool
