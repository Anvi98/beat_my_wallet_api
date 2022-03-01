from datetime import datetime
import json
from numpy import deprecate
import pandas as pd
from passlib.context import CryptContext

# Hashing password and Verify password:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
  return pwd_context.hash(password)

def verify(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

#Save Json file requested
def save_json(res_json):
  # should use epoch time when doing an update on this function
  name= str(datetime.now())
  name = name.split('.')[0].split(' ')
  name = '_'.join(name)
  dstamp = 'data_'+ name

  with open(f"{dstamp}.json", "w") as f:
      json.dump(res_json, f)
  
  return dstamp

def normalization(data_json, trnx):
  with open(f'{data_json}.json','r') as f:
    data = json.loads(f.read())
  df = pd.json_normalize(data, record_path=['result'])
  if trnx == 'erc20':
    features = ['timeStamp','blockNumber','value', 'gasUsed', 'from', 'to']
  if trnx == 'intern':
    features = ['timeStamp','blockNumber','type','value', 'gasUsed', 'from', 'to']

  custom_data = df[features]
  custom_data = custom_data.apply(pd.to_numeric, errors='ignore')

  return custom_data