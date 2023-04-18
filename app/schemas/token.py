from datetime import datetime

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str | None = None
    email: str | None = None
    name: str | None = None
    isAdmin: bool | None = None

class TokenData(BaseModel):
    username: str | None = None
