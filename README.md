# FastAPI Expense Tracker

A REST API for managing and tracking expenses, built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Pydantic**.

## Features

* Add a new expense
* View all expenses
* View an expense by ID
* Filter expenses by category, date, title, and amount
* Delete an expense
* Request validation using Pydantic
* Response models
* PostgreSQL database integration
* SQLAlchemy ORM
* Interactive API documentation with Swagger UI

## Technologies Used

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Uvicorn

## Project Structure

```text
Fastapi project/
│
├── main.py
├── database.py
├── database_models.py
├── schemas.py
├── .gitignore
├── README.md
├── requirements.txt
└── .env
```

## API Endpoints

### Add Expense

```http
POST /post_expenses
```

Adds a new expense to the database.

### Get All Expenses

```http
GET /expenses
```

Returns all expenses.

Supports filtering by:

* Category
* Date
* Title
* Amount

Example:

```http
GET /expenses?category=Food
```

### Get Expense by ID

```http
GET /expenses/{id}
```

Returns a specific expense using its ID.

Example:

```http
GET /expenses/1
```

### Delete Expense

```http
DELETE /delete_expenses/{id}
```

Deletes an expense using its ID.

Example:

```http
DELETE /delete_expenses/1
```

## Database

This project uses **PostgreSQL** as the database and **SQLAlchemy** as the ORM.

Database configuration is stored in environment variables using a `.env` file.

```env
DATABASE_URL=your_database_connection_string
```

The `.env` file is excluded from Git using `.gitignore` to prevent sensitive information from being uploaded.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory:

```env
DATABASE_URL=your_database_connection_string
```

### 6. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

## Validation

The API uses **Pydantic** for request validation.

Invalid or missing request data can result in a:

```text
422 Unprocessable Entity
```

response.

## Future Improvements

* JWT authentication
* Pagination
* Sorting
* Expense analytics
* Monthly expense reports
* Automated testing
* Docker support

## Author

**Akash Santhosh**

Computer Science and Engineering