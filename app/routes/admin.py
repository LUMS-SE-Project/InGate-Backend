from fastapi import APIRouter
from app.config.db import client

router = APIRouter()

@router.post('/')
async def path1(data: dict):
    try:
        table = client["SEProj"]["Admin"] # what collection, what table
        table.insert_one(data)
        return {"message": "Data inserted successfully"}
    except Exception as e:
        return {"error": "Error: %s" % e}
    

@router.post('/signup')
async def path2(data: dict):
    return {"message": "Signup Endpoint for Admin"} 

@router.post('/login')
async def path3(data: dict):
    return {"message": "Login Endpoint for Admin"}



