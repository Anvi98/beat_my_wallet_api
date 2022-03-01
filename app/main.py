import time
from fastapi import FastAPI, APIRouter
from . collect import *
from . utils import *
from . routers import erc20, internal, user, auth
from .database import engine
from . import models
import psycopg2
from psycopg2.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


## Connect to DB:
while True:
  try:
    conn = psycopg2.connect(host='localhost', database='bmw', user='postgres', password='root12', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was successful')
    break
  except Exception as error:
    print("Connecting to Database failed")
    print("Error: ", error)
    time.sleep(2)



app.include_router(erc20.router)
app.include_router(internal.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
def welcome():
  return {"Success": "You're successfully connected to your wallet"}



