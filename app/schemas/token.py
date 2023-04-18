from datetime import datetime

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    display_name: str | None = None

class TokenData(BaseModel):
    username: str | None = None
