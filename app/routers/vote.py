
from fastapi import FastAPI, HTTPException, Depends
import app


from pydantic import BaseModel

from typing import Optional
from .. import models, schemas
from ..database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.oauth2 import get_current_user
import app

from fastapi import APIRouter

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=201)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=409, detail="Vote already exists")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed"}
