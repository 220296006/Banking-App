from typing import Annotated
import uvicorn
from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status

import authentication
import models
from authentication import get_current_user
from database import SessionLocal, engine

# Create the FastAPI app
app = FastAPI()
app.include_router(authentication.router)
models.Base.metadata.create_all(bind=engine)

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: None, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}


class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email


class HomeLoanInput:
    def __init__(self, principal: float, interest_rate: float, years: int):
        self.principal = principal
        self.interest_rate = interest_rate
        self.years = years

class InvestmentInput:
    def __init__(self, principal: float, interest_rate: float, years: int):
        self.principal = principal
        self.interest_rate = interest_rate
        self.years = years


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
