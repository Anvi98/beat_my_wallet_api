from fastapi import FastAPI, APIRouter
from . collect import *
from . utils import *
from . routers import erc20, internal, user, auth
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# For now, we'll allow all CORS, but we'll talk about it on meeting
origins = ["*"]
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins= origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


app.include_router(erc20.router)
app.include_router(internal.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
def welcome():
  return {"Success": "You're successfully connected to your wallet"}



