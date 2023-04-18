import regex as re
from app.config.db import client
from app.schemas.user import User, UserInDB

async def verify_email(email : str):
    e = email
    # regex to match the format of email containing @lums.edu.pk
    r = r"^[a-zA-Z0-9_.+-]+@lums.edu.pk$"

    # check if the email is valid
    if(re.search(r, e)):
        pass
    else:
        raise Exception("Invalid email")

    # check if the email is registered
    table = client["SEProject"]["User"]

    # if the email is already registered, raise an error
    if(table.find_one({"email": e})):
        return
    else:
        raise Exception("Email not found")

async def get_password(email : str):
    table = client["SEProject"]["User"]

    # get the hashed password from db
    hashed_password = table.find_one({"email": email})["hashed_password"]

    if (hashed_password):
        return hashed_password
    else:
        raise Exception("Email not found")
    
async def get_info(email : str):
    table = client["SEProject"]["User"]
    user = table.find_one({"email": email})

    if not user:
        raise Exception("Email not found")
    user = UserInDB(**user)
    return user