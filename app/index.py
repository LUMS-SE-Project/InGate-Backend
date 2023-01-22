# import fast APi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# create a route
@app.get("/")
def index():
    return {"data": {"name": "John"}}


@app.get("/test")
def test():
    return {"Hello World!"}
