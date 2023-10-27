# Banking Application

![Alt text](<Fast Money.png>)

## Table of Contents

- [Introduction](#introduction)
- [Tech Stack](#tech-stack)
- [Backend](#back-end)
- [Frontend](#front-end)
- [Features](#features)
- [API Endpoint](#api-endpoints)
- [Usage](#usage)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Conclusion](#conclusion)

## Introduction

The Banking Application is a web-based banking system that allows users to perform deposit and withdrawal transactions, track their account activity, and view their account balance. This README provides an overview of the application, including its tech stack and key requirements.

## Tech Stack

The following technologies are used in this project:'

- **Frontend:**

  - Angular TypeScript

- **Backend:**

  - Python (Flask or Django)

- **Database:**
  - Text files for storing bank data and transaction logs

## Back-End

The back-end of the Banking App is developed using Python and FastAPI. It provides API endpoints for user authentication and financial calculations.

### Prerequisites

- Python 3.6+
- Dependencies listed in `requirements.txt`
- SQL database (configured in `app.py`)

### Setting Up

1. Clone this repository:

   ```shell
   git clone https://github.com/220296006/banking-app.git
   cd banking-app/back-end

   ```

2. Create a virtual environment (optional but recommended):

```python

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```

3. Install dependencies:

```python

pip install -r requirements.txt

```

4. Run the FastAPI application:

```python

uvicorn main:app --host 127.0.0.1 --port 8000

```

## Front-End

The front-end of the Banking App is built using Angular. It provides a user interface for login and accessing financial tools.

Prerequisites

- Node.js
- Angular CLI
-

### Setting Up

1. Navigate to the front-end folder:

```shell

cd banking-app/front-end

```

2. Install dependencies:

```shell

npm install

```

3. Start the Angular development server:

```shell

ng serve

```

## Features

- User authentication via JWT tokens.
- Home loan calculation.
- Investment calculation.
- CORS middleware for cross-origin requests.

## Project Structure

src/app/components: Angular components.
src/app/services: Services for making API requests.
src/app/model: Data models.

## Usage

Access the front-end at <http://localhost:4200>.
Log in using valid credentials.
Use the provided features to calculate home loans and investments.

## API Endpoints

- POST /login: User login and token generation.
- GET /user/: Get user details.
- POST /calculate-home-loan/: Calculate home loan.
- POST /calculate-investment/: Calculate investment.

## Functional Requirements

1. Users can log in to their accounts securely.
2. Users can initiate deposit and withdrawal transactions.
3. The application reads and updates account balances stored in a "Bank Data.txt" file.
4. All transactions are logged in a "Transaction Log.txt" file with timestamps.
5. Users can view their current account balance after each transaction.
6. Proper error handling is implemented for user input validation.

## Non-Functional Requirements

1. **Security:**

   - User data is securely stored and transmitted.
   - Implement user authentication and authorization.
   - Protect against common web vulnerabilities.

2. **Responsive Design:**

   - The application should be responsive and work on various devices and screen sizes.

3. **Performance:**

   - Optimize the application for efficient rendering and minimal loading times.
   - Implement appropriate caching strategies.

4. **User Experience:**

   - Create a user-friendly and intuitive user interface.
   - Implement accessibility features for users with disabilities.

5. **Scalability:**
   - Ensure that the application can handle a growing number of users and transactions.

## Conclusion

This Banking Application provides a simple yet functional banking system that allows users to manage their accounts securely. It employs a tech stack comprising Angular TypeScript for the frontend and Python for the backend. Functional and non-functional requirements have been defined to ensure that the application is secure, responsive, and user-friendly.

For detailed installation and usage instructions, please refer to the project's documentation.
