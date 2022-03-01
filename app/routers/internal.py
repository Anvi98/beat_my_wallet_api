# Internal Trnx
from app.collect import *
from app.utils import normalization, save_json
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. database import get_db
from .. import oauth2,models, schemas

router = APIRouter(
  prefix= "/trnx/intern",
  tags=["Intern Transactions"]
)

trnx='intern'

@router.get("/")
def basic_bulk_tranx(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
  list_data = []

  url = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={address_list[0]}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={api_key}'

  # Api Calls and saving of json data
  result = api_collect(url)
  list_data += [save_json(result)]

  # normalise json to dataframe for processing
  df = normalization(list_data[0], trnx)  

  date_last_trnx = get_date_last_trnx(df)
  low = low_trnx(df)
  high = high_trnx(df)
  first = first_trnx(df)
  last = last_trnx(df)
  type_trnx = get_type_last_trnx(df)
  from_tranx = get_from_to_last_trnx(df)[0]
  to_trnx = get_from_to_last_trnx(df)[-1]

  response = {
    "date_of_trnx": date_last_trnx,
    "low_trnx": low ,
    "high_trnx": high,
    "first_trnx": first, 
    "last_trnx": last,
    "type_trnx": type_trnx,
    "from": from_tranx,
    "to": to_trnx
  }
  return {"Data": response}


@router.get('/all-stats')
def get_stats(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  stats = db.query(models.Statistic).all()
  return stats

@router.get('/stats/')
def get_query(address: str, category: str, frequence: str, db: Session = Depends(get_db)):
  url = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={api_key}'
  # Api Calls and saving of json data
  list_data = []
  result = api_collect(url)
  list_data += [save_json(result)]

  # normalise json to dataframe for processing
  df = normalization(list_data[0], trnx)

  cat = category
  frq = frequence
  
  # Check if category and frequence exists in DB
  try:
    temp_cat= db.query(models.UserChoiceStat).filter(models.UserChoiceStat.label == cat).first()
    if not temp_cat:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Any category of such request found.")
    temp_fr = db.query(models.Frequence).filter(models.Frequence.frequence == frq).first()
    if not temp_fr:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Any frequence of such type found.")
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Something went wrong in the request.")

  #
  if cat ==  'highest_trade' and frq == 'origin':
    high = high_trnx(df)
  else:
    high= "not found"
  return {"highest transaction since origin": high }



