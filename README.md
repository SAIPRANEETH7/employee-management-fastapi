# Employee Management API

A RESTful Employee Management API built using **FastAPI**, **Pydantic**, **SQLAlchemy**, and **MySQL**.

This project was developed as part of a backend development assignment. The first version used temporary in-memory Python list storage. In Task 2, the application was updated to use MySQL database storage through SQLAlchemy so that employee records persist even after the application is restarted.

---

## Features

- Create, read, update, and delete employee records
- MySQL database persistence
- SQLAlchemy ORM for database operations
- Automatic employee ID generation
- Automatic `created_at` timestamp
- `is_active` defaults to `true`
- Email format validation
- Case-insensitive email uniqueness
- Database-level unique constraint on email
- Rejects empty or whitespace-only required fields
- `WFH` / `WFO` work mode validation
- Proper HTTP status codes and error messages
- Database transaction rollback on failed operations
- Automatic database session cleanup
- Interactive Swagger UI documentation

---

## Technology Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **MySQL**
- **SQLAlchemy**
- **PyMySQL**
- **python-dotenv**
- **Uvicorn**
- **Swagger UI**
- **Git & GitHub**

---

## Project Structure

```text
Fast-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

Use 