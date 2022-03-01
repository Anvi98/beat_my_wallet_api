from sqlalchemy.orm import Session
from app.database import get_db
from app import utils
from .. import schemas, models
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

#create New user
@router.post('/create', status_code = status.HTTP_201_CREATED, response_model= schemas.UserDataOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  new_user = models.User(**user.dict())
  print(new_user.role)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user
