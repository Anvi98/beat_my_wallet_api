from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import database, schemas, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY
SECRET_KEY = settings.secret_key
# ALGORITHM USED
ALGORITHM = settings.algorithm
# EXPIRATION TIME
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":  expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt 

def verify_access_token(token: str, credential_exception):

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    id:str = payload.get("user_id")
    role:str = payload.get("role")

    if id is None:
      raise credential_exception

    token_data =  schemas.TokenData(id=id, role=role)

  except JWTError:
    raise credential_exception
  
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  token = verify_access_token(token, credential_exception)
  user = db.query(models.User).filter(models.User.id == token.id).first()

  return user