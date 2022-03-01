from app.collect import *
from app.utils import normalization, save_json
from fastapi import APIRouter
# ERC_20 Tranx
router = APIRouter(
  prefix="/trnx/erc20",
  tags=["ERC20 Transactions"]
)

@router.get("/")
def get_last_erc20():
  list_data = []
  trnx = 'erc20'
  url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address_list[0]}&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'
 
  result = api_collect(url)
  list_data += [save_json(result)]

  # normalise json to dataframe for processing
  df = normalization(list_data[0], trnx)

  date_last_trnx = get_date_last_trnx(df)
  low = low_trnx(df)
  high = high_trnx(df)
  first = first_trnx(df)
  last = last_trnx(df)
  from_tranx = get_from_to_last_trnx(df)[0]
  to_trnx = get_from_to_last_trnx(df)[-1]

  response = {
    "date_of_trnx": date_last_trnx,
    "low_trnx": low ,
    "high_trnx": high,
    "first_trnx": first, 
    "last_trnx": last,
    "from": from_tranx,
    "to": to_trnx
  }
  return {"Data": response}