from fastapi import APIRouter
from app.config.db import client
from app.schemas.admin import Admin
from app.schemas.user import Login
from app.schemas.user import User
from app.schemas.user import ItemRequest
from app.schemas.restaurant import Item
from app.schemas.user import Reported
from app.schemas.user import ItemAccept

from bson import ObjectId



router = APIRouter()


@router.post('/signup')
def create(data: Admin):
    try:
        data = dict(data)
        table = client["SEProject"]["Admin"]  # what collection, what table
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
def check(data: Login):
    data = dict(data)
    data_all = all_admins()
    for i in data_all:
        if (i["username"] == data["username"] and i["password"] == data["password"]):
            return {"login": "Login successful"}
    return {"login": "Invalid password/username"}


@router.get('/signupRequests')
def display_reqs():
    response = client["SEProject"]["User"].find({})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        if (i["status"] == False):
            data.append(i)
    return data




@router.put('/verify_status')
def verifyS(data: User):
    data = dict(data)
    data["status"] = True
    data = client["SEProject"]["User"].update_one(
        {"email": data["email"]}, {"$set": data})
    return "Done"


@router.put('/reject_user')
def rejectUser(data: User):
    data = dict(data)
    data = client["SEProject"]["User"].delete_one({"email": data["email"]})
    return {"message":"Done"}



@router.put('/verify_alumnus')
def verifyA(data: User):
    data = dict(data)
    data["alumnus"] = True
    data = client["SEProject"]["User"].update_one(
        {"username": data["username"]}, {"$set": data})
    return "Done"




@router.get('/all-item-requests')
def all_item_requests():
    response = client["SEProject"]["ItemRequest"].find({"accepted": 0})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return {"all-requested-items": data}

# accept item request
@router.put('/accept-item-request')
def accept_item_request(item: ItemAccept):
    item_table = client["SEProject"]["ItemRequest"]
    item = dict(item)
    item_table.update_one({"_id": ObjectId(item["item_id"])}, {"$set": {"accepted": 1}})

    
    item_table = client["SEProject"]["Item"]
    item_table.insert_one(dict(item))


    return {"message": "Item Request Accepted"}

# reject item request
@router.post('/reject-item-request')
def reject_item_request(item: ItemAccept):
    item_table = client["SEProject"]["ItemRequest"]
    item = dict(item)
    item_table.delete_one({"_id": ObjectId(item["item_id"])})
    return {"message": "Item Request Rejected"}

# view all reported users
@router.get('/all-reported-users')
def all_reported_users():
    response = client["SEProject"]["Reported"].find({"approved_by_admin": 0})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return {"all-reported-users": data}

# approve reported user
@router.post('/approve-reported-user')
def approve_reported_user(user: Reported):
    # set the status in the user table as false
    user_table = client["SEProject"]["User"]
    user = dict(user)
    user_table.update_one({"email" : user["reportee_email"]}, {"$set": {"status": False}})

    # remove from the reported table
    reported_table = client["SEProject"]["Reported"]
    reported_table.update_one({"reportee_email" : user["reportee_email"], "reporter_email": user["reporter_email"]} , {"$set": {"approved_by_admin" : 1}})

    return {"message": "User Blocked"}

# reject approved user
@router.post('/reject-reported-user')
def reject_reported_user(user: Reported):
    # remove the user from the reported table
    user_table = client["SEProject"]["Reported"]
    user = dict(user)
    user_table.delete_one({"reportee_email" : user["reportee_email"], "reporter_email": user["reporter_email"]})
    return {"message": "User Removed From The reported Table"}


