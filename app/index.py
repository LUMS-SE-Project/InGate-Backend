# import fast APi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import db config stored in core folder
from app.core.db import connect_mongodb

# create an instance of the app
app = FastAPI()

origins = [
    *["http://localhost:3000"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect to mongodb
client = connect_mongodb()



# create a route
@app.get("/")
def index():
    return {"data": {"name": "John"}}


@app.get("/test")
def test():
    return {"Hello World!"}


# create a table if not exists in the db and handles errors
def create_table():
    try:
        db = client["SEProj"]
        table = db["test"]
        return table
    except Exception as e:
        print("Error: %s" % e)
        


table = create_table()