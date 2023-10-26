from datetime import datetime, timedelta
import jwt
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

# Configure CORS settings
origins = ['http://localhost:4200']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT token
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Set token expiration time


# Models for request and response data
class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Endpoint for user login
@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


class HomeLoanData(BaseModel):
    principal: float
    interest_rate: float
    loan_term: int


class InvestmentData(BaseModel):
    investment_amount: float
    annual_interest_rate: float
    years: int


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


# Endpoint to calculate Home Loan
@app.post("/calculate-home-loan/")
async def calculate_home_loan_endpoint(
        principal: float = Form(...),
        interest_rate: float = Form(...),
        loan_term: int = Form(...),
):
    # Calculate Home Loan
    result = calculate_home_loan(principal, interest_rate, loan_term)
    return result


# Endpoint to calculate Investment
@app.post("/calculate-investment/")
async def calculate_investment_endpoint(
        investment_amount: float = Form(...),
        annual_interest_rate: float = Form(...),
        years: int = Form(...),
):
    # Calculate Investment
    result = calculate_investment(investment_amount, annual_interest_rate, years)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
