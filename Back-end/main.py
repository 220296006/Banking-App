from datetime import datetime, timedelta, timezone
from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Verify password and get user functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# Authenticate user function
def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create access token function
def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency for getting the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Dependency for getting the current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# User login endpoint
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint to get the current user
@app.get("/user", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# Endpoint to get the current user's items
@app.get("/users/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


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
