from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from typing import Optional
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import app


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

import app.routers.post as post
import app.routers.users as users
import app.routers.auth as auth

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)




