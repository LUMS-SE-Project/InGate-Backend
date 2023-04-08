from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel


class Admin(BaseModel):
    username : str
    email : str | None = None
    password : str | None = None
