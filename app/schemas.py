from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
  email: EmailStr
  password: str
  role: str

class UserDataOut(BaseModel):
  id: int
  role: str
  email: EmailStr
  created_at: datetime

  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

  class Config:
    orm_mode = True

class Token(BaseModel):
  access_token: str
  token_type: str

  class Config:
    orm_mode : str

class TokenData(BaseModel):
  id : Optional[str] = None
  role: Optional[str] = None
