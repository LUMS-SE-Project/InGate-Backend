from fastapi import APIRouter
from app.config.db import client
from app.schemas.admin import Admin
from app.schemas.user import Login
from app.schemas.user import User


router = APIRouter()

@router.post('/signup')
def create(data: Admin):
    try:
        data = dict(data)
        table = client["SEProject"]["Admin"] # what collection, what table
        table.insert_one(data)
        return {"message": "Data inserted successfully"}
    except Exception as e:
        return {"error": "Error: %s" % e}

def all_admins():
    response = client["SEProject"]["Admin"].find({})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

@router.post('/login')
def check(data:Login):
    data = dict(data)
    data_all = all_admins()
    for i in data_all:
        if(i["username"] == data["username"] and i["password"]== data["password"]):
           return {"login": "Login successful"}
    return {"login": "Invalid password/username"}
    
@router.get('/signupRequests')
def display_reqs():
    response = client["SEProject"]["User"].find({})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        if(i["status"]== False):
            data.append(i)
    return data

@router.put('/verify_status')
def verifyS(data:User):
    data = dict(data)
    data["status"] = True
    data = client["SEProject"]["User"].update_one({"username": data["username"]}, {"$set":data})
    return "Done"
    

@router.put('/verify_alumnus')
def verifyA(data:User):
    data = dict(data)
    data["alumnus"] = True
    data = client["SEProject"]["User"].update_one({"username": data["username"]}, {"$set":data})
    return "Done"


# @router.post('/signup')
# async def path2(data: dict):
#     return {"message": "Signup Endpoint for Admin"} 

# @router.post('/login')
# async def path3(data: dict):
#     return {"message": "Login Endpoint for Admin"}



