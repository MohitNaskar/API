from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from .. import models, schemas
from ..utils import verify_password

router = APIRouter(prefix="/auth",
                   tags=["auth"])

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

