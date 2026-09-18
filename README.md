# Employee Management API

A RESTful backend application for managing employee records using **FastAPI, Pydantic, SQLAlchemy, and MySQL**.

This project was developed as part of a backend development assignment. In Task 1, employee records were stored temporarily in a Python list. In Task 2, the application was upgraded to use MySQL database storage through SQLAlchemy so that employee records persist even after the application is restarted.

---

## Features

- Create employee records
- Retrieve all employees
- Retrieve an employee by ID
- Update employee records
- Delete employee records
- MySQL database persistence
- SQLAlchemy ORM
- Automatic employee ID generation
- Automatic `created_at` timestamp
- `is_active` defaults to `true`
- Email format validation
- Case-insensitive email uniqueness
- Duplicate email requests are rejected
- Database-level unique constraint on email
- Rejects empty and whitespace-only required fields
- `WFH` and `WFO` work mode validation
- Proper HTTP status codes
- Clear validation and error responses
- Database transaction rollback on failures
- Database session cleanup
- Automatic `employees` table creation
- Interactive Swagger API documentation

---

## Technology Stack

- Python
- FastAPI
- Pydantic
- MySQL
- SQLAlchemy
- PyMySQL
- python-dotenv
- Uvicorn
- Swagger UI
- Git
- GitHub

---

## Project Structure

```text
employee-management-fastapi/
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

