from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel


class User(BaseModel):
    username : str
    email : str | None = None
    name : str | None = None
    password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None

class UserInDB(BaseModel):
    username : str
    email : str | None = None
    name : str | None = None
    hashed_password : str | None = None
    alumnus : bool | None = None
    status : bool | None = None

class Login(BaseModel):
    username: str
    password: str
