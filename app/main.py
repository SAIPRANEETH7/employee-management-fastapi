from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .schemas import Employee, EmployeeCreate
from .services import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
)


app = FastAPI(
    title="Employee Management API",
    description="Backend API for managing employee records.",
    version="2.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "Application is running."}


@app.post(
    "/employees",
    response_model=Employee,
    status_code=status.HTTP_201_CREATED,
)
def create_new_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_employee(db, employee_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@app.get("/employees", response_model=list[Employee])
def list_employees(
    db: Session = Depends(get_db),
):
    return get_all_employees(db)


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):

    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than zero.",
        )

    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return employee


@app.put("/employees/{employee_id}", response_model=Employee)
def update_existing_employee(
    employee_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
):

    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than zero.",
        )

    try:
        employee = update_employee(
            db,
            employee_id,
            employee_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return employee


@app.delete("/employees/{employee_id}")
def delete_existing_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):

    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than zero.",
        )

    deleted = delete_employee(db, employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return {"message": "Employee deleted successfully."}