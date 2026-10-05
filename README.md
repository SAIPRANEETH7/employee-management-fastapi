# Employee Management API

A RESTful Employee Management Backend API built with FastAPI, Pydantic, SQLAlchemy, MySQL, and PyMySQL.

The project has been extended through four stages:

- **Task 1:** Employee records were stored temporarily in a Python list.
- **Task 2:** Employee records were migrated to MySQL using SQLAlchemy ORM with persistent CRUD operations.
- **Task 3:** The employee list endpoint was extended with SQLAlchemy-based search, filtering, sorting, and pagination.
- **Task 4:** Work items were added with employee foreign-key assignments, relationships, CRUD endpoints, and filtered pagination.

## Features

- Create, view, update, and delete employees
- Health check endpoint
- MySQL persistence using SQLAlchemy ORM
- Automatic employee ID generation
- Pydantic validation
- Case-insensitive unique email handling
- Database-level unique email constraint
- Database transaction rollback and error handling
- Automatic table creation on startup
- Search employees by partial name, ignoring case
- Filter by department
- Filter by WFH/WFO
- Filter by active/inactive status
- Limit and offset pagination
- SQLAlchemy-side filtering and pagination without loading all employees into Python
- Ascending employee ID ordering
- Swagger UI documentation and testing

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API framework |
| Pydantic | Request/response validation |
| SQLAlchemy | ORM and database queries |
| MySQL | Relational database |
| PyMySQL | MySQL driver |
| Uvicorn | ASGI server |
| python-dotenv | Environment configuration |
| Swagger UI | API documentation/testing |
| Git | Version control |
| GitHub | Repository hosting |

## Project Structure

```text
employee-management-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── Screenshots/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

`.env` is local-only and is excluded from Git. Virtual environments and Python cache files are also excluded.

## Prerequisites

- Python 3.12
- MySQL Server
- MySQL Workbench
- Git
- VS Code

Check Python:

```powershell
python --version
```

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/SAIPRANEETH7/employee-management-fastapi.git
cd employee-management-fastapi
```

### 2. Create and activate the virtual environment

```powershell
python -m venv NewEnv
NewEnv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create the MySQL database

In MySQL Workbench:

```sql
CREATE DATABASE employee_management;
USE employee_management;
```

The application creates the `employees` table automatically at startup using SQLAlchemy metadata.

### 5. Configure `.env`

Create `.env` in the project root:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_management
```

Replace `YOUR_PASSWORD` with the local MySQL password. If the password contains URL-reserved characters, encode them in the connection URL.

`.env.example` contains the template without the real password.

### 6. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

## Database Model

The `employees` table contains:

| Column | Description |
|---|---|
| `id` | Auto-increment primary key |
| `name` | Employee name |
| `email` | Unique employee email |
| `department` | Employee department |
| `primary_skill` | Main skill |
| `location` | Employee location |
| `work_mode` | `WFH` or `WFO` |
| `is_active` | Active status |
| `created_at` | Creation timestamp |

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/employees` | Create employee |
| GET | `/employees` | Search, filter, and paginate employees |
| GET | `/employees/{employee_id}` | Get one employee |
| PUT | `/employees/{employee_id}` | Update employee |
| DELETE | `/employees/{employee_id}` | Delete employee |

## Task 3 - Search, Filtering and Pagination

The existing `GET /employees` endpoint now accepts optional query parameters. All filtering, counting, ordering, limit, and offset operations are performed by SQLAlchemy/database queries. The application does not load all employees into a Python list and filter them in memory.

### Query Parameters

| Parameter | Type | Default | Allowed values / behavior |
|---|---|---:|---|
| `search` | string | `null` | Partial employee-name search; case-insensitive |
| `department` | string | `null` | Exact department filter |
| `work_mode` | enum | `null` | `WFH` or `WFO` |
| `is_active` | boolean | `null` | `true` or `false` |
| `limit` | integer | `10` | 1 to 100 |
| `offset` | integer | `0` | 0 or greater |

Filters can be used individually or together.

### Search Example

```text
GET /employees?search=rah
```

The search is partial and case-insensitive. For example, `rah` and `RAH` can match `Rahul Sharma`.

### Department Filter

```text
GET /employees?department=Engineering
```

### Work Mode Filter

```text
GET /employees?work_mode=WFH
```

### Active Status Filter

```text
GET /employees?is_active=true
```

or:

```text
GET /employees?is_active=false
```

### Pagination

```text
GET /employees?limit=5&offset=0
```

The next page can be requested with:

```text
GET /employees?limit=5&offset=5
```

`limit` controls the maximum number of records returned. `offset` controls how many matching records are skipped.

### Combined Filters

```text
GET /employees?department=Engineering&work_mode=WFH&is_active=true&limit=5&offset=0
```

This returns up to five active Engineering employees who work from home.

### Response Format

```json
{
  "total": 3,
  "limit": 5,
  "offset": 0,
  "items": [
    {
      "name": "Ananya Reddy",
      "email": "ananya.reddy@example.com",
      "department": "Engineering",
      "primary_skill": "Java",
      "location": "Bengaluru",
      "work_mode": "WFH",
      "is_active": true,
      "id": 11,
      "created_at": "2026-09-16T03:38:59"
    }
  ]
}
```

- `total` is the number of matching records before pagination.
- `limit` is the requested page size.
- `offset` is the requested number of skipped records.
- `items` contains the current page.

If there are no matches, the API returns `200 OK` with `total: 0` and `items: []`. If the offset is beyond the matching records, `total` remains correct and `items` is empty.

## Validation and Error Handling

### Employee validation

- Required string fields cannot be empty or whitespace-only.
- Email must be valid.
- Email is normalized to lowercase.
- Email must be unique, case-insensitively.
- `work_mode` must be `WFH` or `WFO`.
- Employee IDs must be greater than zero.

### Task 3 query validation

- `limit=0` is rejected.
- `limit` values greater than 100 are rejected.
- Negative `limit` values are rejected.
- Negative `offset` values are rejected.
- Unsupported `work_mode` values are rejected.
- Invalid boolean values for `is_active` are rejected by FastAPI/Pydantic.

FastAPI returns validation errors with HTTP `422` for parameter validation failures.

### Common status codes

| Status | Meaning |
|---:|---|
| 200 | Successful request |
| 201 | Employee created |
| 400 | Invalid request or duplicate email |
| 404 | Employee not found |
| 422 | Validation error |
| 500 | Database/server failure |

## SQLAlchemy Query Implementation

The Task 3 list query is built dynamically. Conditions are added only when the corresponding query parameter is provided.

The service then:

1. Builds the base `select(Employee)` query.
2. Adds the name search condition when `search` is supplied.
3. Adds department filtering when supplied.
4. Adds work-mode filtering when supplied.
5. Adds active-status filtering when supplied.
6. Counts the matching records before pagination.
7. Orders by `Employee.id.asc()`.
8. Applies `offset`.
9. Applies `limit`.
10. Returns the total and current page.

This ensures search, filtering, and pagination are performed by the database rather than by loading all rows into Python.

## Task 1 to Task 2 to Task 3

### Task 1

Employee data was stored in a temporary Python list. Restarting the application removed the data.

### Task 2

The list was replaced with MySQL persistence using SQLAlchemy ORM. CRUD operations now use the database, with sessions, transactions, rollback handling, and database-level email uniqueness.

### Task 3

The `GET /employees` endpoint was extended with SQLAlchemy-based name search, department filtering, work-mode filtering, active-status filtering, record counting, ordering, limit, and offset pagination. Existing create, get-by-ID, update, and delete operations remain available.

## Testing Performed

The Task 3 endpoint was tested using Swagger UI for:

- Default pagination
- `limit` and `offset` pagination
- Partial employee-name search
- Case-insensitive employee-name search
- Department filtering
- WFH/WFO filtering
- Active/inactive filtering
- Combined filters
- No matching records
- Offset beyond the matching records
- Invalid `limit` values
- Negative `offset`
- Invalid `work_mode`
- Existing CRUD endpoints after the Task 3 changes

The application also retains the Task 2 tests for duplicate email, employee-not-found, invalid ID, whitespace validation, and database persistence.

## Sample Test Data

Fictional employee records were used to test different departments, work modes, active states, and multiple pagination pages.

Examples include Engineering, Backend, Product, Cybersecurity, QA, Finance, DevOps, Human Resources, and Data Science employees, with both WFH and WFO records and both active and inactive records.

## API Test Evidence

`Screenshots/` retains the Task 1–3 evidence and includes six Task 4 request/response evidence images generated from actual local HTTP exchanges. Each image shows the request, actual status, and response body. Observed results: create existing employee `201`; nonexistent employee `404`; get/search/filter/combined filters/pagination `200`; invalid status, invalid priority, and blank title `422`; missing item `404`; reassignment `200`; deletion `204`; existing employee CRUD/list and health endpoints `200`. The list was queried again after stopping and restarting Uvicorn; work-item rows remained available.

### Create a work item

![POST /work-items, actual 201 response with assigned employee](Screenshots/Task4-Create-201.svg)

### Combined filters

![GET /work-items with combined filters and actual response](Screenshots/Task4-Combined-Filters-200.svg)

### Blank title validation

![POST /work-items with whitespace title, actual 422 response](Screenshots/Task4-Blank-Title-422.svg)

### Assignment to a nonexistent employee

![POST /work-items with nonexistent employee, actual 404 response](Screenshots/Task4-Employee-Not-Found-404.svg)

### Reassign and update

![PUT /work-items with reassignment, actual 200 response](Screenshots/Task4-Reassign-Update-200.svg)

### Delete

![DELETE /work-items, actual 204 response with empty body](Screenshots/Task4-Delete-204.svg)

## What I Learned

- How FastAPI query parameters work.
- How to validate query parameters using `Query`.
- How to use Pydantic enums for allowed values.
- How to build dynamic SQLAlchemy queries.
- How to perform case-insensitive searches with `ilike`.
- How to combine multiple SQLAlchemy filters.
- How SQL `COUNT`, `ORDER BY`, `LIMIT`, and `OFFSET` relate to API pagination.
- How to calculate the total before pagination.
- How to return a consistent paginated response.
- Why filtering and pagination should be performed in the database instead of in Python memory.

## Difficulties Faced

The main difficulty in Task 3 was implementing search, filtering, and pagination without loading all employee records into Python. The solution was to construct the query dynamically with SQLAlchemy and let the database perform the filtering, counting, ordering, offset, and limit operations.

Another consideration was preserving the existing Task 2 CRUD behavior while changing the response format of `GET /employees`. A separate `EmployeeListResponse` schema was added so the list endpoint can return `total`, `limit`, `offset`, and `items`.

## Assumptions

- MySQL Server is running locally.
- The database is named `employee_management`.
- The local MySQL user has permission to create and access the database/table.
- Employee data used for testing is fictional.
- Authentication, frontend development, Docker, table relationships, and migrations are outside the scope of this task.

## Git Workflow

Check changes:

```powershell
git status
```

Stage changes:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Implement employee search filtering and pagination"
```

Push changes:

```powershell
git push
```

## Repository

GitHub repository:

https://github.com/SAIPRANEETH7/employee-management-fastapi

## Task 4 - Work Items and Employee Relationship

Task 4 adds persistent work items assigned to existing employees. The `work_items.employee_id` column is a foreign key to `employees.id`, and the SQLAlchemy `Employee.work_items` / `WorkItem.assigned_employee` relationships expose the connection in both directions. An employee must exist before a work item can be created or reassigned. Work-item list filtering, counting, ordering, and pagination are performed in SQLAlchemy queries.

### Work item table

| Column | Description |
|---|---|
| `id` | Auto-increment primary key |
| `title` | Required, trimmed, non-blank title (up to 200 characters) |
| `description` | Optional text |
| `employee_id` | Required foreign key to `employees.id` |
| `status` | `TODO`, `IN_PROGRESS`, or `COMPLETED`; defaults to `TODO` |
| `priority` | `LOW`, `MEDIUM`, or `HIGH`; defaults to `MEDIUM` |
| `due_date` | Optional date (`YYYY-MM-DD`) |
| `created_at` | Automatically generated timestamp |

`create_all()` creates the new table when the application starts. It does not alter existing tables; this task adds a new table only.

### Work item endpoints

| Method | Endpoint | Success |
|---|---|---|
| POST | `/work-items` | `201 Created` |
| GET | `/work-items` | `200 OK`, paginated list |
| GET | `/work-items/{work_item_id}` | `200 OK` |
| PUT | `/work-items/{work_item_id}` | `200 OK`; accepts the fields to change |
| DELETE | `/work-items/{work_item_id}` | `204 No Content` |

Every item response includes its assigned employee's `id`, `name`, and `email` in `assigned_employee`.

Create example:

```http
POST /work-items
Content-Type: application/json
```

```json
{
  "title": "Prepare weekly status report",
  "description": "Summarize project progress",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-15"
}
```

List query parameters:

| Parameter | Behavior |
|---|---|
| `search` | Partial, case-insensitive match on title |
| `employee_id` | Assigned employee ID; must be positive |
| `status` | `TODO`, `IN_PROGRESS`, or `COMPLETED` |
| `priority` | `LOW`, `MEDIUM`, or `HIGH` |
| `limit` | Defaults to 10; range 1–100 |
| `offset` | Defaults to 0; must be 0 or greater |

Example combined filter and page:

```text
GET /work-items?search=weekly&employee_id=2&status=TODO&priority=MEDIUM&limit=10&offset=0
```

List responses use this shape; `total` counts all matches before pagination, and items are ordered by ascending ID:

```json
{
  "total": 1,
  "limit": 10,
  "offset": 0,
  "items": [
    {
      "id": 1,
      "title": "Prepare weekly status report",
      "description": "Summarize project progress",
      "employee_id": 2,
      "status": "TODO",
      "priority": "MEDIUM",
      "due_date": "2026-10-15",
      "created_at": "2026-09-29T12:00:00",
      "assigned_employee": {
        "id": 2,
        "name": "Employee Name",
        "email": "employee@example.com"
      }
    }
  ]
}
```

Update example (fields are optional, so this can also reassign an item):

```http
PUT /work-items/1
Content-Type: application/json
```

```json
{"employee_id": 3, "status": "IN_PROGRESS", "priority": "HIGH"}
```

### Validation and error cases

- Unknown employee on create or reassignment: `404 Not Found`.
- Missing work-item ID: `404 Not Found`.
- Invalid status or priority, blank title, non-positive employee ID, invalid date, or invalid pagination values: `422 Unprocessable Entity`.
- Deleting an item succeeds with an empty `204` response.
- Invalid or duplicate employee data continues to use the existing employee endpoint behavior.
- The foreign key uses `ON DELETE RESTRICT`; an employee with work items cannot be removed at the database level until those items are removed.

### Task 4 verification and screenshots

The Task 4 test pass should cover creation for a real employee, nonexistent employee, retrieval by ID, case-insensitive partial search, individual and combined filters, pagination, reassignment/update, invalid status/priority/title, missing IDs, deletion, application restart persistence, and employee API regression checks. Capture Swagger UI screenshots showing the request, HTTP status, and response body for representative success and validation/error cases in `Screenshots/`.

### What I learned and difficulties

This task demonstrates a one-to-many relationship: an employee can own multiple work items, and each work item points to one employee through a database-enforced foreign key. SQLAlchemy relationships allow response serialization to include basic employee details without duplicating employee columns in the work-item table. The main implementation challenge is preserving referential integrity while allowing assignments and performing combined filters/counting/pagination in database queries.

The main Task 4 learning was how a foreign key and ORM relationship connect independently stored records while supporting nested response details. A challenge was building a combined list query whose count is computed before pagination and whose related employee is loaded efficiently. Validation also needs to reject null updates for required database fields while still allowing optional descriptions and due dates to be cleared.

### Assumptions

- Existing MySQL connection settings and employee table are reused.
- Status and priority values are uppercase enum strings.
- PUT applies only supplied fields, allowing focused edits and reassignment.
- Deleting an employee that still has work items is restricted by the foreign key.

## Version

```text
Task 4
Employee Management API
Version 4.0.0
```

## Summary

Task 4 extends the Employee Management API with employee-assigned work items, a foreign key and SQLAlchemy relationship, validation, CRUD endpoints, and database-side search, filtering, ordering, counting, and pagination. Existing employee endpoints remain available.

Thank You.