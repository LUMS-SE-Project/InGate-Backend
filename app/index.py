from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.db import client

app = FastAPI(title="InGate")

origins = [
    *["https://localhost:3000"],
    *["https://localhost:8081"],
    *["https://localhost:8080"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes.index import router as IndexRouter
from app.routes.admin import router as AdminRouter
from app.routes.user import router as UserRouter


app.include_router(IndexRouter, tags=["Base"])
app.include_router(AdminRouter, prefix="/admin", tags=["Admin"])
app.include_router(UserRouter, prefix="/user", tags=["User"])