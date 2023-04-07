from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends

from app.schemas.user import User

router = APIRouter()

@router.get("/")
def index():
    return {"message": "Hello World!"}

# @router.get("/protected")
# # async def protected(token: Annotated[str, Depends(auth_scheme)]):
#     return {"token": token}

# @router.get("/token")
# async def token():
#     return 

# @router.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user