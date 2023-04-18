from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import User, UserInDB
from app.schemas.user import Login
from app.config.db import client

from app.auth.provider import oauth2_scheme, get_password_hash
from app.utils.signUp import verify_email

router = APIRouter()


@router.get('/')
async def path1():
    return {"message": "User Endpoint"}


@router.post('/signup')
async def create(data : User):
    try :
        await verify_email(data.email)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
    
    hashed_password = get_password_hash(data.password)

    # create an object for the db insertion
    db_obj = UserInDB(
        username=data.username, 
        email=data.email, 
        name=data.name, 
        hashed_password=hashed_password, 
        alumnus=data.alumnus, 
        status=data.status
        )
    table = client["SEProject"]["User"]

    try:
        table.insert_one(db_obj)
    except Exception as e:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{e}"
        )

    return {"signup": "Signup successful"}



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
            # return the token
            user = i
            if(i["status"] == True):
                return {"login": "Login successful"}
            else:
                return {"login": "Account unverified"}
            
    return {"login": "Invalid password/username"}
    

