# FastAPI Expense Tracker

A backend Expense Tracker API built with **FastAPI**, **SQLAlchemy**, **SQLite**, **Pydantic**, and **JWT authentication**.

The application allows users to securely register and log in, create and manage their own expenses, filter and sort expenses, paginate results, and validate incoming data.

The project also includes a comprehensive **pytest** test suite covering authentication, CRUD operations, validation, filtering, pagination, sorting, authorization, token expiration, and edge cases.

---

## Features

- User registration
- Secure password hashing using bcrypt
- User login with JWT authentication
- JWT token expiration
- Token validation
- User-specific expense management
- Create expenses
- Retrieve expenses
- Update expenses
- Delete expenses
- Expense filtering
- Pagination
- Sorting
- Request validation using Pydantic
- Database relationships using SQLAlchemy
- Protected API endpoints
- Authentication and authorization
- Duplicate username validation
- Expired token handling
- Edge-case handling
- Automated testing using pytest
- Interactive API documentation using Swagger UI and ReDoc

---

## Technologies Used

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyJWT
- Passlib
- bcrypt
- python-dotenv
- pytest
- HTTPX

---

## Project Structure

```text
FastAPI-Expense-Tracker/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── dependencies.py
├── conftest.py
│
├── routers/
│   ├── users.py
│   └── expenses.py
│
├── tests/
│   ├── test_users.py
│   ├── test_expenses.py
│   └── test_edge_cases.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Application Architecture

The application follows a modular backend architecture.

```text
Client
  │
  ▼
FastAPI Routes
  │
  ├── Authentication
  │
  ├── User Operations
  │
  └── Expense Operations
  │
  ▼
Dependencies
  │
  ├── Database Session
  │
  └── JWT Authentication
  │
  ▼
Pydantic Schemas
  │
  ▼
SQLAlchemy Models
  │
  ▼
SQLite Database
```

---

## Authentication

The application uses JWT (JSON Web Token) based authentication.

### Registration

A new user can register using a username and password.

The password is never stored directly in the database. Instead:

```text
Plain Password
      │
      ▼
Password Hashing
      │
      ▼
Hashed Password
      │
      ▼
Database
```

Passwords are hashed using **bcrypt** before being stored.

### Login

Users can log in using their username and password.

The authentication flow is:

```text
Username + Password
        │
        ▼
    Find User
        │
        ▼
 Verify Password
        │
        ▼
   Generate JWT
        │
        ▼
 Return Access Token
```

The JWT contains information such as:

- User ID
- Username
- Expiration time

### JWT Token Expiration

Every access token has an expiration time. The token payload contains an `exp` claim.

When an expired token is used:

```text
Request
   │
   ▼
JWT Verification
   │
   ▼
Token Expired
   │
   ▼
401 Unauthorized
```

Expired tokens cannot be used to access protected endpoints.

### Authorization

Expense endpoints are protected using JWT authentication. A user's token determines their identity. Users can only access their own expenses.

For example:

```text
User A
  │
  ├── Expense 1
  ├── Expense 2
  └── Expense 3

User B
  │
  ├── Expense 4
  └── Expense 5
```

User A cannot access or modify User B's expenses.

---

## Database

The application uses SQLAlchemy ORM for database interaction.

Two main entities are used:

```text
User
 │
 │ 1
 │
 │
 │ *
 ▼
Expense
```

A single user can have multiple expenses.

### User Model

The user table contains:

- id
- username
- hashed_password

### Expense Model

The expense table contains:

- id
- title
- amount
- category
- date
- user_id

The `user_id` column acts as a foreign key connecting each expense to its owner.

---

## Expense CRUD Operations

The API supports complete CRUD functionality:

- Create
- Read
- Update
- Delete

### Create Expense

Users can create a new expense by providing:

- Title
- Amount
- Category
- Date

The authenticated user's ID is automatically associated with the expense.

### Get Expenses

Authenticated users can retrieve their expenses. Only expenses belonging to the authenticated user are returned.

### Update Expense

Users can update an existing expense. The update operation supports partial updates, meaning users do not necessarily have to provide every field.

For example, only the category can be changed while keeping the title, amount, and date unchanged.

### Delete Expense

Users can delete their own expenses. The API verifies that the expense belongs to the authenticated user before deleting it.

---

## Filtering

The API supports filtering expenses using query parameters.

Supported filters include:

- Title
- Category
- Date
- Amount

Examples:

```text
GET /expenses?title=Food
GET /expenses?category=Travel
GET /expenses?date=2026-08-19
GET /expenses?amount=500
```

Filters can also be combined:

```text
GET /expenses?category=Food&title=Lunch
```

---

## Pagination

Pagination is implemented to prevent returning an unnecessarily large number of records at once.

Pagination uses parameters such as:

- skip
- limit

Example:

```text
GET /expenses?skip=0&limit=10
```

This retrieves the first page of expenses.

Another example:

```text
GET /expenses?skip=10&limit=10
```

This retrieves the next set of expenses.

---

## Sorting

Expenses can be sorted based on supported fields, in ascending or descending order.

Expenses can be sorted by fields such as:

- Amount
- Date
- Title
- Category

---

## Validation

Request data is validated using Pydantic. Validation helps prevent invalid data from entering the application.

Examples of validated data include:

- Required fields
- Amount values
- Dates
- String fields
- Update payloads

Invalid requests return appropriate HTTP validation errors instead of being inserted directly into the database.

---

## Edge Case Testing

The project includes dedicated edge-case tests to verify that the application behaves correctly under unusual or boundary conditions.

The edge-case tests cover scenarios such as:

- **Duplicate Usernames** — the application prevents multiple users from registering with the same username.
- **Expired JWT Tokens** — the application rejects expired authentication tokens and returns an unauthorized response.
- **Invalid Authentication** — invalid credentials and invalid authentication tokens are rejected appropriately.
- **Very Large Expense Amounts** — the application is tested with very large numerical expense values.
- **Boundary Values** — boundary and unusual input values are tested to ensure the API handles them correctly.
- **Multiple Expenses Belonging to the Same User** — the application is tested with multiple expenses belonging to the same authenticated user to ensure that retrieval, filtering, updating, and deletion operate on the correct records.
- **User Authorization** — users cannot access, update, or delete expenses belonging to another user.

---

## Testing

The project uses **pytest** for automated testing.

The test suite covers:

- User registration
- Duplicate username handling
- Login
- Invalid credentials
- Password verification
- JWT generation
- JWT validation
- Expired tokens
- Protected endpoints
- User authorization
- Expense creation
- Expense retrieval
- Expense updating
- Expense deletion
- Filtering
- Pagination
- Sorting
- Validation
- Multiple expenses
- Edge cases
- Authentication failures

### Test Fixtures

`conftest.py` is used to provide reusable pytest fixtures.

The fixtures help with:

- Test database setup
- Database sessions
- Test client
- User creation
- Authentication
- Test isolation

The tests use a separate testing database/session so that testing does not affect the main application database.

### Running Tests

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the complete test suite:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Expected result:

```text
47 passed
```

---

## Environment Variables

Sensitive configuration values are stored in environment variables instead of being hard-coded into the source code.

Example `.env` file:

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file should not be committed to Git.

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd FastAPI-Expense-Tracker
```

### 2. Create a Virtual Environment

Using Python 3.11:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Application

Start the FastAPI application using:

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to:

- View endpoints
- View request parameters
- Send API requests
- Test authentication
- Test CRUD operations
- Inspect responses

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

ReDoc provides another interface for exploring the API documentation.

---

## API Endpoints

### Authentication / User Endpoints

| Method | Endpoint | Description         | Authentication |
|--------|----------|----------------------|-----------------|
| POST   | /users   | Register a new user  | No              |
| POST   | /login   | Login and receive JWT| No              |

### Expense Endpoints

| Method | Endpoint   | Description               | Authentication |
|--------|------------|----------------------------|-----------------|
| POST   | /expenses  | Create an expense          | Required        |
| GET    | /expenses  | Retrieve user's expenses   | Required        |
| PUT    | /expenses  | Update an expense          | Required        |
| PATCH  | /expenses  | Partially update an expense| Required        |
| DELETE | /expenses  | Delete an expense          | Required        |

### Authentication Header

Protected endpoints require a JWT access token.

The token is sent using the HTTP Authorization header:

```text
Authorization: Bearer <access_token>
```

In Swagger UI, the token can be provided through the Authorize functionality.

---

## Example Workflow

A typical user workflow is:

```text
1. Register
      │
      ▼
2. Login
      │
      ▼
3. Receive JWT Access Token
      │
      ▼
4. Authenticate Protected Requests
      │
      ▼
5. Create Expenses
      │
      ▼
6. Retrieve Expenses
      │
      ▼
7. Filter / Sort / Paginate
      │
      ▼
8. Update Expenses
      │
      ▼
9. Delete Expenses
```

---

## Security

The project implements several security-related practices:

- Password hashing
- JWT-based authentication
- Token expiration
- Protected endpoints
- User-specific data access
- Authorization checks
- Environment variables for sensitive configuration
- Validation of incoming request data

Passwords are never stored as plain text. JWT tokens are required for protected expense operations.

---

## Error Handling

The API returns appropriate HTTP status codes for different situations.

Examples include:

| Code | Meaning |
|------|---------|
| 200  | OK |
| 201  | Created |
| 400  | Bad Request |
| 401  | Unauthorized |
| 404  | Not Found |
| 422  | Unprocessable Entity |

Authentication failures and invalid or expired tokens are handled appropriately.

---

## Git and Version Control

The project is maintained using Git.

The repository includes:

- Source code
- Test suite
- Dependency configuration
- Environment configuration
- Documentation

Sensitive files such as `.env` are excluded from version control using `.gitignore`.

The project includes dedicated edge-case tests.

---

## Project Highlights

This project demonstrates practical backend development skills including:

- REST API development
- FastAPI
- Python
- SQLAlchemy ORM
- Database relationships
- Pydantic validation
- JWT authentication
- Password hashing
- Authorization
- Dependency injection
- CRUD operations
- Query filtering
- Pagination
- Sorting
- Error handling
- Automated testing
- Pytest fixtures
- Edge-case testing
- Environment configuration
- Git version control

---

## Future Improvements

Potential future improvements include:

- PostgreSQL deployment
- Alembic database migrations
- Refresh token implementation
- Expense analytics
- Monthly and yearly reports
- Category-based statistics
- Budget management
- Docker containerization
- CI/CD integration
- Cloud deployment
- API rate limiting

---

## Conclusion

The FastAPI Expense Tracker is a modular backend application designed to demonstrate real-world API development practices.

It combines authentication, authorization, database management, validation, CRUD operations, filtering, pagination, sorting, and automated testing into a single backend project.

The project has been thoroughly tested with a pytest test suite, including dedicated edge-case testing, to verify that the application behaves correctly across normal, invalid, boundary, and authentication-related scenarios.

## Author

**Akash Santhosh**

Computer Science and Engineering