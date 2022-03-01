from fastapi import requests
from datetime import datetime
import requests

address_list = ['0x3839C0A0FE5b55117788D628Fb803cB6c27ad544','0x0BDA046968c97347C6154f59013f059cA88Bb03A'] 
api_key = 'MG9HZYXENZCY7HGTIXH9BG7BTTP6MDIAGX'

def api_collect(url):
  response = requests.get(url)
  if response.status_code == 200:
    res = response.json()
    return res
  else:
    return 'no response'


# Bulk Info Transactions : General
def first_trnx(df):
  return float(df['value'][0])

def last_trnx(df):
  list_val = df['value'].values.tolist()
  return float(list_val[-1])

def low_trnx(df):
  return float(df['value'].min())

def high_trnx(df):
  return float(df['value'].max())


def get_date_last_trnx(df):
  last_trx = df['timeStamp'].values.tolist()
  ts = last_trx[-1]
  date = datetime.fromtimestamp(ts)
  return date

def get_type_last_trnx(df):
  type_last_trnx = df['type'].values.tolist()
  return str(type_last_trnx[-1])

def get_from_to_last_trnx(df):
  from_last_trnx = df['from'].values.tolist()
  from_last_trnx = from_last_trnx[-1]
  to_last_trnx = df['to'].values.tolist()
  to_last_trnx = to_last_trnx[-1]
  return str(from_last_trnx), str(to_last_trnx)