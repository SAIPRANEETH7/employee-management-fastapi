from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import create_tables, get_db
from .schemas import EmployeeCreate, EmployeeResponse
from .services import create_employee, get_employee, list_employees

app = FastAPI(title="Employee Service", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    create_tables()


@app.get("/health")
def health():
    return {"status": "ok", "service": "employee"}


@app.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def post_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return create_employee(db, data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    try:
        return list_employees(db)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    if employee_id <= 0:
        raise HTTPException(status_code=400, detail="Employee ID must be greater than zero.")
    try:
        employee = get_employee(db, employee_id)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
