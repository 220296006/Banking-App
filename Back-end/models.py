from sqlalchemy import Column, Integer, String
from database import Base


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class HomeLoans(Base):
    __tablename__ = 'Home Loans'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    monthly_payment = Column(Integer)
    total_payment = Column(Integer)
    total_interest = Column(Integer)

class Investments(Base):
    __tablename__ = 'Investment'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    future_value = Column(Integer)

