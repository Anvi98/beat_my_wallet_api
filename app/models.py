from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Statistic(Base):
  __tablename__= "statistics"

  id = Column(Integer, primary_key=True, nullable=False)
  blockchain_name = Column(String, nullable=False)
  address_wallet = Column(String, nullable=False)
  category_request = Column(String, nullable=False)
  id_user_choice_stat = Column(Integer, ForeignKey("choice_user_stats.id", ondelete="CASCADE"), nullable=False)
  id_frequence = Column(Integer, ForeignKey("frequences.id", ondelete="CASCADE"), nullable=False)
  result_stat = Column(String, nullable=False)
  generated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

class UserChoiceStat(Base):
  __tablename__ = "choice_user_stats"
  id = Column(Integer, primary_key=True, nullable=False)
  label = Column(String, nullable=False, unique= True)

class Frequence(Base):
  __tablename__ = "frequences"
  id = Column(Integer, primary_key=True, nullable=False)
  frequence = Column(String, nullable=False)

class User(Base):
  __tablename__= "users"
  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  role = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
