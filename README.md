# Employee Management API

A RESTful Employee Management Backend API built using FastAPI, Pydantic, SQLAlchemy, and MySQL.

This project was developed in two stages:

- Task 1: Employee data stored temporarily in a Python list.
- Task 2: Employee data migrated to MySQL using SQLAlchemy ORM for permanent data persistence.

The API provides complete CRUD operations for managing employee records.

---

# Features

- Create a new employee
- Retrieve all employees
- Retrieve an employee by ID
- Update an existing employee
- Delete an employee
- Health check endpoint
- Automatic employee ID generation
- MySQL database persistence
- SQLAlchemy ORM
- Pydantic request validation
- Email format validation
- Case-insensitive email handling
- Database-level unique email constraint
- Work mode validation
- Required field validation
- Empty and whitespace-only field validation
- Proper HTTP status codes
- Database transaction rollback
- Database failure handling
- Automatic `employees` table creation
- Environment variable based database configuration
- Swagger UI for API testing

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| FastAPI | Web framework |
| Pydantic | Data validation |
| SQLAlchemy | ORM and database operations |
| MySQL | Relational database |
| PyMySQL | MySQL database driver |
| Uvicorn | ASGI server |
| python-dotenv | Environment variable management |
| Swagger UI | API documentation and testing |
| Git | Version control |
| GitHub | Source code repository |
| VS Code | Development environment |

---

# Project Structure

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
├── Screenshots/
│   ├── POST-create.png
│   ├── GET-all.png
│   ├── GET-by-id.png
│   ├── PUT-update.png
│   ├── DELETE.png
│   ├── duplicate-email.png
│   ├── employee-not-found.png
│   ├── invalid-id.png
│   ├── invalid-work-mode.png
│   ├── persistence-before-restart.png
│   ├── persistence-after-restart.png
│   ├── mysql-table.png
│   └── database-error.png
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md