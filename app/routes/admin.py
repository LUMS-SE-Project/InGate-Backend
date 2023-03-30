from fastapi import APIRouter
from app.config.db import client

admin = APIRouter()

admin.post('/admin')
def admin(data: dict):
    # insert value into Admin table in the database
    try:
        table = client["SEProj"]["Admin"]
        table.insert_one(data)
        return {"message": "Data inserted successfully"}
    except Exception as e:
        return {"error": "Error: %s" % e}

