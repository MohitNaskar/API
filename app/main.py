from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
# from . import models
# from .database import engine


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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





