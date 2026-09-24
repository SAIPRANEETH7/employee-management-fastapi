from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from .database import create_tables, get_db
from .schemas import Employee, EmployeeCreate, EmployeeListResponse
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
    version="3.0.0",
)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/health")
def health_check():
    return {"status": "Application is Running Successfully."}


@app.get(
    "/employees",
    response_model=EmployeeListResponse,
)
def list_employees(
        search: str | None = Query(
            default=None,
            description="Search employees by name. Partial and case-insensitive.",
        ),
    department: str | None = Query(
        default=None,
        description="Filter employees by department.",
    ),
    work_mode: str | None = Query(
        default=None,
        description="Filter by WFH or WFO.",
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filter by employee active status.",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip.",
    ),
    db: Session = Depends(get_db),
):
    if work_mode is not None:
        work_mode = work_mode.upper()

        if work_mode not in {"WFH", "WFO"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="work_mode must be either WFH or WFO.",
            )

    try:
        total, employees = get_all_employees(
            db=db,
            search=search,
            department=department,
            work_mode=work_mode,
            is_active=is_active,
            limit=limit,
            offset=offset,
        )

        return EmployeeListResponse(
            total=total,
            limit=limit,
            offset=offset,
            items=employees,
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )


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

    try:
        employee = get_employee_by_id(db, employee_id)

    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found.",
        )

    return employee

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

    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )
        
        
        
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

    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found.",
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

    try:
        deleted = delete_employee(db, employee_id)

    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found.",
        )

    return {"message": f"Employee Id {employee_id} deleted successfully."}