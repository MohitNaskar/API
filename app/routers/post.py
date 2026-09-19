from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.oauth2 import get_current_user, oauth2_scheme

from typing import Optional
from .. import models, schemas
from ..database import engine, get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import app

from fastapi import APIRouter

router = APIRouter(prefix="/posts",
                   tags=["posts"])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = None,
):
    posts_query = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id)
    if search:
        posts_query = posts_query.filter(models.Post.title.ilike(f"%{search}%"))
    posts = posts_query.limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_post = models.Post(
        user_id=current_user.id,
        **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

@router.get("/latest", response_model=schemas.Post)
def get_latest_post(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=404, detail="No posts available")
    return  post

@router.get("/me", response_model=List[schemas.Post])
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{id}", status_code=204)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )
    updated_post.title = post.title
    updated_post.content = post.content
    updated_post.published = post.published
    db.commit()
    db.refresh(updated_post)
    return updated_post