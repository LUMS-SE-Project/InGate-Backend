from fastapi import APIRouter
from app.schemas.user import User
from app.schemas.user import Login
from app.config.db import client
router = APIRouter()


@router.get('/')
async def path1():
    return {"message": "User Endpoint"}


@router.post('/signup')
def create(data:User):
    data = dict(data)
    table = client["SEProject"]["User"]
    table.insert_one(data)
    return {"message": "Data inserted successfully"}


def all():
    response = client["SEProject"]["User"].find({})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

@router.post('/login')
def check(data:Login):
    data = dict(data)
    data_all = all()
    for i in data_all:
        if(i["username"] == data["username"] and i["password"]== data["password"]):
            if(i["status"] == True):
                return {"login": "Login successful"}
            else:
                return {"login": "Account unverified"}
    return {"login": "Invalid password/username"}
    