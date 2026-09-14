
from fastapi import FastAPI, HTTPException, Depends
import app


from pydantic import BaseModel

from typing import Optional
from .. import models, schemas
from ..database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import app

from fastapi import APIRouter

router = APIRouter(prefix="/users",
                   tags=["users"])

@router.post("/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)
    user_data = user.model_dump(exclude={"id"})
    user_data["password"] = hashed_password
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

