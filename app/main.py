from fastapi import FastAPI

from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

import app.routers.post as post
import app.routers.users as users
import app.routers.auth as auth
import app.routers.vote as vote

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)





