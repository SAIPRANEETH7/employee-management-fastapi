from fastapi import FastAPI, HTTPException, status

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
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "Application is running"}


@app.post(
    "/employees",
    response_model=Employee,
    status_code=status.HTTP_201_CREATED,
)
def create_new_employee(employee_data: EmployeeCreate):

    for employee in get_all_employees():
        if employee.email == employee_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )

    return create_employee(employee_data)


@app.get("/employees", response_model=list[Employee])
def list_employees():
    return get_all_employees()


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):

    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than zero.",
        )

    employee = get_employee_by_id(employee_id)

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
):

    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than zero.",
        )

    employee = get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    for existing_employee in get_all_employees():
        if (
            existing_employee.email == employee_data.email
            and existing_employee.id != employee_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )

    return update_employee(employee_id, employee_data)


@app.delete("/employees/{employee_id}")
def delete_existing_employee(employee_id: int):

    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than zero.",
        )

    deleted = delete_employee(employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return {"message": "Employee deleted successfully."}