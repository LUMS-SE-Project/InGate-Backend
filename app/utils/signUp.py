from fastapi import HTTPException, status
import regex as re
from app.config.db import client

async def verify_email(email : str):
    # regex to match the format of email containing @lums.edu.pk
    regex = r"^[a-zA-Z0-9_.+-]+@lums.edu.pk$"

    # check if the email is valid
    if(re.search(regex, email)):
        pass
    else:
        raise Exception("Invalid email")

    # check if the email is already registered
    table = client["SEProject"]["User"]

    # if the email is already registered, raise an error
    if(table.find_one({"email": email})):
        raise Exception("Email already registered")

    return True



