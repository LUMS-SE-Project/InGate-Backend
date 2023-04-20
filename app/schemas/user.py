from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from app.schemas.restaurant import ItemInCart


class User(BaseModel):
    username : str | None = None
    email : str
    name : str | None = None
    password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None
    isAdmin : bool | None = None
    gender: str 

class UserInSignUp(BaseModel):
    username : str
    email : str
    name : str
    password : str
    alumnus : bool

class UserInDB(BaseModel):
    username : str | None = None
    email : str
    name : str | None = None
    hashed_password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None
    gender: str
    isAdmin : bool | None = None

class Login(BaseModel):
    username: str
    password: str

class Order(BaseModel):
    items: list[ItemInCart]
    gender_preference: str
    partial_order: bool

class ItemRequest(BaseModel):
    item_name: str
    item_location: str
    requester_email: str
    accepted: bool

class Reviews(BaseModel):
    reviewer_email: str
    reviewee_email: str
    review: str
    rating: int

class Blocked(BaseModel):
    blocker_email: str
    blockee_email: str