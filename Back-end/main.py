import os
from datetime import datetime, timedelta
from typing import List

import jwt
import uvicorn
from dotenv import dotenv_values, load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select, Session
from starlette import status

import auth
from auth import Token, pwd_context, SECRET_KEY, ALGORITHM
from database import engine, User

# Load environment variables
credentials = dotenv_values(".env")
load_dotenv()

# Create the FastAPI app
app = FastAPI()
app.include_router(auth.router)
# Configure CORS settings
origins = ['http://localhost:4200']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for Settings
class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("AUTHJWT_SECRET_KEY",
                                        'c134a520d4e3e665e7f2a6aa2f1834a9f9075b1e06e65e3d37c5368394fc0320')


def get_session():
    with Session(engine) as session:
        yield session


# Verify password and get user functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username, password):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    user = session.execute(select(User).where(User.username == username)).first()
    if user and verify_password(password, user[0].password):
        session.close()
        return True

    session.close()
    return False


def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


@AuthJWT.load_config
def get_config():
    return Settings()


@app.post("/login", response_model=Token)
async def login(username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        access_token = create_access_token({"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username/password")


# Endpoint to get the current users
@app.get("/user", response_model=List[User])
async def fetch_user(session: Session = Depends(get_session)):
    statement = select(User)
    result = session.exec(statement).all()
    return result


# Function to calculate home loan
def calculate_home_loan(principal, interest_rate, loan_term):
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    monthly_payment = principal * (
            (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments)
            / ((1 + monthly_interest_rate) ** num_payments - 1)
    )
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - principal
    return {
        "monthly_payment": monthly_payment,
        "total_payment": total_payment,
        "total_interest": total_interest,
    }


# Function to calculate investment
def calculate_investment(investment_amount, annual_interest_rate, years):
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    num_months = years * 12
    future_value = investment_amount * (1 + monthly_interest_rate) ** num_months
    return {"future_value": future_value}


# API endpoint to calculate Home Loan
@app.post("/calculate-home-loan/")
async def calculate_home_loan_endpoint(
        principal: float = Form(...),
        interest_rate: float = Form(...),
        loan_term: int = Form(...),
        username: str = Form(...)
):
    result = calculate_home_loan(principal, interest_rate, loan_term)
    with open("home_loan_results.txt", "a") as file:
        file.write(f"Username: {username}, Home Loan Result: {result}\n")
    return result


# API endpoint to calculate Investment
@app.post("/calculate-investment/")
async def calculate_investment_endpoint(
        investment_amount: float = Form(...),
        annual_interest_rate: float = Form(...),
        years: int = Form(...),
        username: str = Form(...)
):
    result = calculate_investment(investment_amount, annual_interest_rate, years)
    with open("investment_results.txt", "a") as file:
        file.write(f"Username: {username}, Investment Result: {result}\n")
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
