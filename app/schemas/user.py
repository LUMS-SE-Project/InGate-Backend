
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
    number : str


class User(BaseModel):
    username : str | None = None
    email : str
    name : str | None = None
    password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None
    isAdmin : bool | None = None
    gender: str 

class UserInDB(BaseModel):
    username : str | None = None
    email : str
    name : str | None = None
    hashed_password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None
    gender: str | None = None
    isAdmin : bool | None = None
    number : str | None = None

class Login(BaseModel):
    username: str
    password: str

class Order(BaseModel):
    items: list[ItemInCart]
    gender_preference: str
    partial_order: bool
    order_email: str

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

class Reported(BaseModel):
    reporter_email: str
    reportee_email: str
    situation: str
    additional_comments: str
    approved_by_admin: int
    # 0 would mean not approved
    # 1 would mean approved

class ItemAccept(BaseModel):
    item_id: str
    item_name: str
    item_location: str
    requester_email: str
    accepted: bool