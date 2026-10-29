from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .models import Employee
from .schemas import EmployeeCreate


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    try:
        exists = db.scalar(select(Employee.id).where(func.lower(Employee.email) == data.email.lower()))
        if exists is not None:
            raise ValueError("Email already exists.")
        employee = Employee(
            name=data.name,
            email=data.email,
            department=data.department,
            primary_skill=data.primary_skill,
            location=data.location,
            work_mode=data.work_mode.value,
            is_active=data.is_active,
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except ValueError:
        db.rollback()
        raise
    except IntegrityError as error:
        db.rollback()
        raise ValueError("Email already exists.") from error
    except SQLAlchemyError as error:
        db.rollback()
        raise RuntimeError("Database operation failed.") from error


def list_employees(db: Session) -> list[Employee]:
    try:
        return list(db.scalars(select(Employee).order_by(Employee.id.asc())).all())
    except SQLAlchemyError as error:
        db.rollback()
        raise RuntimeError("Database operation failed.") from error


def get_employee(db: Session, employee_id: int) -> Employee | None:
    try:
        return db.get(Employee, employee_id)
    except SQLAlchemyError as error:
        db.rollback()
        raise RuntimeError("Database operation failed.") from error
