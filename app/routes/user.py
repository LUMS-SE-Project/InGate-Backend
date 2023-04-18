from fastapi import APIRouter
from app.config.db import client

router = APIRouter()


@router.get('/')
async def path1():
    return {"message": "User Endpoint"}
